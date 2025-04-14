# HYSPLIT on Ubuntu/Linux: Installation and Usage Tutorial

This tutorial explains how to download, install, and run HYSPLIT on Ubuntu/Linux, including the process of converting WRF output to a format compatible with HYSPLIT. The reference documentation is available at the [NOAA HYSPLIT Tutorial](https://www.ready.noaa.gov/documents/Tutorial/html/index.html).

---

## 1. Download HYSPLIT

Go to the [HYSPLIT download page](https://www.ready.noaa.gov/HYSPLIT_linuxtrial.php) and download the appropriate trial version for Linux. You will receive a file like:

```
hysplit.vX.Y.Z_OS.tar.gz
```

Replace `X.Y.Z` and `OS` with the actual version and your system's OS.

## 2. Extract the Files

Navigate to the folder where the file was downloaded and extract it:

```bash
tar -xvzf hysplit.vX.Y.Z_OS.tar.gz
```

The program is ready to use; there is no need to run `make`. However, make sure NetCDF libraries are installed on your system.

## 3. Test HYSPLIT

Navigate to the `testing` folder inside the HYSPLIT directory. For example:

```bash
cd /home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.0_UbuntuOS20.04.6LTS/testing
```

Then run the sample script:

```bash
bash xrun.scr
```

After the script finishes, you should see a file called `results.ps`, which provides an example of the output.

---

## 4. Converting WRF Data to ARL Format for HYSPLIT

Place all your `wrfout` files in a dedicated folder. Use the script `convert_art.sh` or call the `arw2arl` executable directly to convert each WRF output file.

### Example:
```bash
/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/./arw2arl wrfout_d01_2022-06-15_00:00:00
```

By default, the output file is named `ARLDATA.BIN`. To keep things organized, rename it using the date of the original WRF file:

```bash
mv ARLDATA.BIN 2022-06-15.BIN
```

Repeat this step for all WRF output files. Once all `.BIN` files are created, concatenate them into one:

```bash
cat 2022-05-31.BIN 2022-06-03.BIN 2022-06-07.BIN 2022-06-11.BIN 2022-06-15.BIN >> join_feedback_1.BIN
```

---

## 5. Edit CONTROL File

Navigate to the `testing` folder:

```bash
cd /home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/testing
```

Edit the `CONTROL.001` file. Here's a breakdown of its structure:

```
Line 1: Start date and time (YY MM DD HH)
Line 2: Number of starting locations and trajectories
Line 3: Latitude, Longitude, and height (m AGL)
Line 4: Duration of the trajectory (negative for backward)
Line 5: Vertical motion method (0 = model vertical velocity)
Line 6: Top of model domain (m)
Line 7: Number of meteorological files
Line 8: Path to meteorological data
Line 9: Meteorological file name
Line 10: Output directory
Line 11: Output file name
```

### Example CONTROL.001
```
00 00 00 00
1
21.44 -16.82 3000.0
192
0
10000.0
1
/home/cometlab/Downloads/delete/wrfout/feedback_1/
join_feedback_1.BIN
./
tdump_001
```

This file configures a 192-hour backward trajectory from (21.44°N, 16.82°W, 3000 m AGL) using the meteorological data in `join_feedback_1.BIN`.

---

## 6. Run the Trajectory

Once your `CONTROL` file is set up, run the trajectory with:

```bash
bash xrun.scr
```

You will get an output file such as `plot_001.ps`, which contains the resulting trajectory plot.

---

## 7. Example Output

![Example Output](https://github.com/user-attachments/assets/570ec631-756d-4146-aaf0-16852ae6efaf)

---

## Notes
- Make sure NetCDF libraries are correctly installed and linked.
- If running into issues, consult the [official tutorial](https://www.ready.noaa.gov/documents/Tutorial/html/index.html).
- This guide is intended for beginners and provides a base to
