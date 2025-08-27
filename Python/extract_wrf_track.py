#!/usr/bin/env python3
"""
extract_wrf_track.py

Finds a hurricane track from WRF output by locating the minimum sea-level pressure (SLP)
for each model time and extracting central pressure and maximum 10-m wind speed near the center.

Outputs:
  - CSV: track_<domain>.csv with columns:
      time_utc, lat, lon, slp_mb, vmax10_kt_in_<R>km, vmax10_kt_domain, i, j, file
  - (optional) KML: track_<domain>.kml if --kml flag is passed

Usage:
  python extract_wrf_track.py --glob "/path/to/wrfout_d03_2005-08-*_00:00:00" --radius_km 100 --kml

Requirements:
  - netCDF4
  - wrf-python (pip install wrf-python)
  - numpy, pandas
  - (optional) simplekml for KML output (pip install simplekml)
"""

import argparse
import glob
import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
from wrf import getvar, ALL_TIMES, to_np, latlon_coords

EARTH_RADIUS_KM = 6371.0

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km for arrays lat2/lon2 to a point lat1/lon1."""
    # Convert to radians
    rlat1, rlon1 = np.radians(lat1), np.radians(lon1)
    rlat2, rlon2 = np.radians(lat2), np.radians(lon2)
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = np.sin(dlat/2.0)**2 + np.cos(rlat1) * np.cos(rlat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS_KM * c

def load_latlon(nc: Dataset):
    """Return 2D lat, lon as numpy arrays (static grid)."""
    slp0 = getvar(nc, "slp", timeidx=0)
    lats, lons = latlon_coords(slp0)
    return to_np(lats), to_np(lons)

def wind10(nc: Dataset, t_idx: int):
    """Return 10-m wind speed (m/s) at time index t_idx as numpy array."""
    u10 = to_np(getvar(nc, "U10", timeidx=t_idx))
    v10 = to_np(getvar(nc, "V10", timeidx=t_idx))
    return np.sqrt(u10**2 + v10**2)

def find_center_and_winds(nc: Dataset, lats2d: np.ndarray, lons2d: np.ndarray, radius_km: float) -> List[Tuple]:
    """
    Iterate over all times in the file and return list of rows:
      (datetime, lat_c, lon_c, slp_c_mb, vmax10_in_r_kt, vmax10_domain_kt, i, j)
    """
    # All times for SLP
    slp_all = getvar(nc, "slp", timeidx=ALL_TIMES)  # Pa or hPa? wrf-python returns hPa (mb)
    slp_all = to_np(slp_all)  # shape (time, y, x)
    # Time coordinate
    time_var = nc.variables.get("Times", None)
    if time_var is not None:
        # "Times" is char array [Time, DateStrLen], decode to str
        times = ["".join(t.astype(str)).strip() for t in time_var[:]]
        # Convert "YYYY-MM-DD_HH:MM:SS" to pandas datetime (UTC)
        times = pd.to_datetime([t.replace("_", " ") for t in times], utc=True)
    else:
        # Fallback: use num2date from any available time var
        # Many WRF files don't have CF time for all vars; we try 'XTIME' in minutes since start
        if "XTIME" in nc.variables:
            xt = nc.variables["XTIME"][:]  # minutes since start
            start = pd.Timestamp("1970-01-01", tz="UTC")
            times = pd.to_datetime(start.value/1e6 + xt*60*1000, unit="ms", utc=True)
        else:
            raise RuntimeError("Could not determine time from WRF file (no Times or XTIME).")

    rows = []
    for t_idx in range(slp_all.shape[0]):
        slp_t = slp_all[t_idx, :, :]
        # find min slp
        ij_min = np.unravel_index(np.nanargmin(slp_t), slp_t.shape)
        i, j = ij_min  # i = y (south_north), j = x (west_east)
        lat_c = float(lats2d[i, j])
        lon_c = float(lons2d[i, j])
        # Force W longitudes negative
        lon_c = -abs(lon_c)

        # Central pressure (wrf-python SLP is in hPa/mb)
        slp_c_mb = float(slp_t[i, j])

        # 10m wind field at same time
        v10 = wind10(nc, t_idx)  # m/s
        # vmax in domain (kt)
        vmax10_domain_kt = float(np.nanmax(v10) * 1.943844)

        # vmax within radius of center
        dist_km = haversine_km(lat_c, lon_c, lats2d, -abs(lons2d))
        mask = dist_km <= radius_km
        if np.any(mask):
            vmax10_in_r = float(np.nanmax(v10[mask]) * 1.943844)
        else:
            vmax10_in_r = np.nan

        rows.append((times[t_idx], lat_c, lon_c, slp_c_mb, vmax10_in_r, vmax10_domain_kt, int(i), int(j)))
    return rows

def process_files(paths: List[str], radius_km: float) -> pd.DataFrame:
    records = []
    latlon_cached = None

    for path in paths:
        with Dataset(path) as nc:
            if latlon_cached is None:
                lats2d, lons2d = load_latlon(nc)
                latlon_cached = (lats2d, lons2d)
            else:
                lats2d, lons2d = latlon_cached

            rows = find_center_and_winds(nc, lats2d, lons2d, radius_km)
            for r in rows:
                records.append({
                    "time_utc": r[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "lat": r[1],
                    "lon": r[2],
                    "slp_mb": r[3],
                    f"vmax10_kt_in_{int(radius_km)}km": r[4],
                    "vmax10_kt_domain": r[5],
                    "i": r[6],
                    "j": r[7],
                    "file": os.path.basename(path),
                })

    df = pd.DataFrame.from_records(records)
    df.sort_values("time_utc", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def write_kml(df: pd.DataFrame, out_path: str):
    try:
        import simplekml
    except ImportError:
        print("simplekml not installed; skipping KML. Run: pip install simplekml")
        return

    kml = simplekml.Kml()
    fol_points = kml.newfolder(name="Track Points")
    fol_line = kml.newfolder(name="Track Line")

    # LineString of the track
    ls = fol_line.newlinestring(name="WRF Track")
    coords = [(float(lon), float(lat)) for lon, lat in zip(df["lon"], df["lat"])]
    ls.coords = coords
    ls.altitudemode = simplekml.AltitudeMode.clamptoground
    ls.style.linestyle.width = 3
    ls.style.linestyle.color = simplekml.Color.red

    # Points
    for _, r in df.iterrows():
        p = fol_points.newpoint(name=r["time_utc"],
                                coords=[(float(r["lon"]), float(r["lat"]))])
        p.description = (f"SLP: {r['slp_mb']:.1f} mb\n"
                         f"Vmax10 in R: {r.filter(like='vmax10_kt_in_').iloc[0]:.1f} kt\n"
                         f"Vmax10 domain: {r['vmax10_kt_domain']:.1f} kt\n"
                         f"i,j: {r['i']},{r['j']}")
        p.timestamp.when = r["time_utc"].replace(" ", "T") + "Z"

    kml.save(out_path)
    print(f"Wrote KML: {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True,
                    help="Glob pattern for wrfout files, e.g., '/ddnA/.../wrfout_d03_2005-08-*_00:00:00'")
    ap.add_argument("--radius_km", type=float, default=100.0, help="Radius (km) for Vmax10 near the center")
    ap.add_argument("--kml", action="store_true", help="Write KML alongside CSV")
    args = ap.parse_args()

    paths = sorted(glob.glob(args.glob))
    if not paths:
        raise SystemExit(f"No files matched: {args.glob}")

    print(f"Found {len(paths)} files.")
    df = process_files(paths, args.radius_km)

    # Infer domain from first file name
    dom = "dXX"
    base = os.path.basename(paths[0])
    if "wrfout_d0" in base:
        try:
            dom = base.split("wrfout_")[1].split("_")[0]
        except Exception:
            pass

    csv_path = f"track_{dom}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Wrote CSV: {csv_path}")

    if args.kml:
        kml_path = f"track_{dom}.kml"
        write_kml(df, kml_path)

if __name__ == "__main__":
    '''
    way of execute
    
    '''
    main()
