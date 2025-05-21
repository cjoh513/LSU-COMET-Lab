# How to Compile `arw2arl` on a Cluster

This guide provides step-by-step instructions to compile the `arw2arl` utility for converting WRF output to ARL format on an HPC system.

---

## 📥 1. Download the Source Code

Download the `hysplit_data2arl.zip` archive from NOAA's official site:

📎 [HYSPLIT data2arl tools](https://www.ready.noaa.gov/HYSPLIT_data2arl.php)  
📦 Direct link: [hysplit_data2arl.zip](https://www.ready.noaa.gov/data/web/models/hysplit4/decoders/hysplit_data2arl.zip)

Then unzip the file:

```bash
unzip hysplit_data2arl.zip
cd hysplit_data2arl
```
🛠️ 2. Prepare the Build Environment
2.1 Move the appropriate Makefile
Move the gfortran-specific Makefile into the correct location:

```bash
Copy
Edit
mv Makefile.inc.gfortran arw2arl/Makefile.inc
```
2.2 Set environment variables for NetCDF
Ensure you have your NetCDF environment variables loaded (via a script like var_env):

```bash
Copy
Edit
source /path/to/var_env  # make sure this sets $NETCDF correctly
```
✏️ 3. Edit the Makefile (Optional)
Open the new Makefile.inc inside arw2arl:

```bash
Copy
Edit
vim arw2arl/Makefile.inc

Ensure it includes these two lines:

make
Copy
Edit
NETINC  = -I$(NETCDF)/include
NETLIBS = -L$(NETCDF)/lib -lnetcdff -lnetcdf
```
These paths ensure that the compiler can find the NetCDF headers and libraries.

📚 4. Add the Missing HYSPLIT Library
You need to provide the libhysplit.a static library. If you already have a compiled version of HYSPLIT:

```bash
Copy
Edit
scp /path/to/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/library/libhysplit.a \
    etorresm@smic.hpc.lsu.edu:/work/etorresm/hysplit_data2arl/metprog/library/
```
This provides the necessary linking library for arw2arl.

🧱 5. Compile the Code
Move into the arw2arl directory and compile:

```bash
Copy
Edit
cd arw2arl
make
```
If everything is set up correctly, this should build the arw2arl executable.

✅ Done!
You now have the arw2arl program compiled and ready to convert WRF output to the ARL format.
