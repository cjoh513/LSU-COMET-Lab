# Table of Contents

1. [Compiling WRF with no Leap Years](#compiling-wrf-with-no-leap-years)  
   - [Configuring](#configuring)  
   - [Altering configure.wrf](#altering-configurewrf)  
   - [Compile](#compile)  

2. [Errors and Solutions](#errors-and-solutions)  
   - [gfortran: error: wrf.o: No such file or directory](#gfortran-error-wrfo-no-such-file-or-directory)  
   - [gcc: error: unrecognized command-line option '-V'](#gcc-error-unrecognized-command-line-option--v)  
   - [error while loading shared libraries: libpng12.so.0](#error-while-loading-shared-libraries-libpng12so0)
   - [Segmentation Fault](#Segmentation-fault)
   - [Efficient WRF Simulation and Domain Decomposition](#Efficient-WRF-Simulation-and-Domain-Decomposition)
   - [Problems of SST of 0 values on the met_em files](#Problems-of-SST-of-0-values-on-the-met_em-files)

3. [If You Delete Your Vtable](#if-you-delete-your-vtable)
4. [Send a process after another on the cluster](Send-a-process-after-another-on-the-cluster)


# Compiling WRF with no Leap Years
This section is dedicated to how to recompile WRF so it skipps leap days (i.e., Feb 29th)
This does assume you've already built the libraries and are either at the "Building WRF" section of the official compilation tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php#STEP8) or you've already compiled WRF

### Configuring
* Navigate to your WRF directory that includes the configure 
![image](https://github.com/user-attachments/assets/b087e575-31ee-453d-b11f-b1b12d1d0495)
* Use "./clean -a" to clean your directory before reconfiguring.  
* Use "./configure" to start the configuration process.  
* Select the "linux x86_64" option or whichever option fits for your systems requirements.  
* Select the "Dmpar for GNU (gfortran/gcc)" or whichever option fits your requirements.  
* Compile for nesting with "nesting: 1=basic".  
* Once configured, open the "configure.wrf" file created during the configuration process.
### Altering configure.wrf
* open configure.wrf with your editor of choice.
* Under the "Architecture specific settings" find the "ARCH_LOCAL" line.
* Add "-DNO_LEAP_CALENDAR".
* Save and close.  
![image](https://github.com/user-attachments/assets/3a8f0ced-b059-4c42-b143-adf37b4bf936)  
### Compile
* compile with "./compile em_real >& log.compile"
* This compiles wrf for real data cases and spits the output compilation output nito the log.compile text file.
* Useful in case there are any errors.
&nbsp;

&nbsp;




# gfortran: error: wrf.o: No such file or directory.  
![image](https://github.com/user-attachments/assets/59d68f7c-989d-4392-83c2-b9a9c31bdf8f)  
This error (or series of them) is most likely a problem of a version mismatch between a version of WRF and the version of GNU.
The only consistent solution I found online and what worked for me was either using an older version of gfortran (which if you're using software on a university's systems might be a non-option) or using an updated version of WRF
&nbsp;

At the time I was trying to recompile wrf3.8 on the university's freshly updated systems-in which they went from redhat 7.9 to 8.8.  
The error was caused because the version of WRF was too old for the updated systems' to deal with.  However, when I compiled WRF 4.2, there were no issues.  
&nbsp;

&nbsp;

# gcc: error: unrecognized command-line option '-V'
A compiling error related to a command that was altered in later versions of gcc.
I found the solution in [THIS](https://forum.mmm.ucar.edu/threads/ubuntu-20-04-configure-netcdf-fortran-4-5-2-error-c-compiler-cannot-create-executables.12707/) forum post.  
The steps outlined by MLandreau in the post worked for me as I was using netcdf-fortran-4.5.2.tar.gz
* from the LIBRARIES directory:
* type what's in the single quotes: 'sed -i "s/$CC -V/$CC -v/g" netcdf-fortran-4.5.2/configure'  
* This replaces "$CC -V" with "$CC -v" in the netcdf configure file.  However this might not fix the problem.
* Open the configure file and go to line 3919.  This is the line right about "$as_echo '$as_me:${as_lineno-$LINENO}: checking for C compiler version" >&5'  
* Above this line add what is in the single quotes ':<<END'  
* Find line 3943 or the lines that end with:
'$as_echo "$as_me:${as_lineno-$LINENO}: \$? = $ac_status" >&5  
test $ac_status = 0; }  
done'  
* Add "END" to the line after "done".
* save and close the configure file.
* if you then run into an error of it unable to find "-lnetcdf" the "LDFLAGS" and "CPPFLAGS" environment variables need to be modified to add the necdf path.
* type "export LDFLAGS=-L$DIR/netcdf/lib"  
* type "export CPPFLAGS=-I$DIR/netcdf/include"  
&nbsp;

&nbsp;

# error while loading shared libraries: libpng12.so.0
./ungrib.exe: error while loading shared libraries: libpng12.so.0: cannot open shared object file: No such file or directory  
This is an ungrib error in which the program cannot find the libpng12.so.0 file despite it being in the directory.  
This error was resolved for me by following [THIS](https://forum.mmm.ucar.edu/threads/resolved-error-while-loading-shared-libraries-libpng12-so-0.193/) forum post  
The "LD_LIBRARY_PATH" needed to be set by the following: "setenv LD_LIBRARY_PATH [full Path to libraries]/grib2/lib:$LD_LIBRARY_PATH"  
This allows for ungrib to locate the path to the lib folder.


# Segmentation Fault
Program received signal SIGSEGV: Segmentation fault - invalid memory reference.  
Often a CFL error, but it might not flag the CFL keyword in the error files.  These errors also tend to crop up well into a simulation so it can be frusterating to deal with.  
[THIS](https://forum.mmm.ucar.edu/threads/sigsegv-segmentation-fault-invalid-memory-reference.8508/) post contains useful steps to try.   
Most often I have solved this error by increasing the "epssm" variable in the namelist.input (e.g., 0.4->0.9).  
The epssm variable relates to vertical wave propogation. If your simulation takes place over complex mountainous terrain or includes some other rapid vertical transport (Hurricanes), a CFL error could be the problem in disguise.  Most recently, this error occurred for me because I had a simulation in December over the continental United States.  A synoptic system was crossing the Rocky Mountains at the time the error threw.  By raising the epssm, the error resolved itself.

<!--
# Domain Size Too Small for This Many Processors for One Domain
Sometimes your domain will be an odd shape or you need more processors than the default wrf formula allows (such as if you were running chemistry).  
If you choose a high number of processors are are met with a "the domain size is too small for this many processors, or the decomposition aspect ratio is poor" error, nproc_x and nproc_y are possible solutions.  
More detailed information, and what to do if you have multiple domains, can be found in the nproc_x_nproc_y.md.
For example.  
![image](https://github.com/user-attachments/assets/57a513a8-1943-4b5f-9380-8c29bb6786c5)  
This error was thrown for a rectangular domain that needed at least 100 processors to run in a reasonable time frame.  
* The solution is to add "nproc_x" and "nproc_y" to the "&domains" section of your namelist.input (I recommend doing so after you've run real.exe as otherwise it will try to distribute the processors while running real.exe and there's probably far more processors during the simulation than the preprocessing stage so it will error).  
* "nproc_x" and "nproc_y" determine the decomposition ratio for your domain, which is to say it alots your domain gridcells per processor.   
* An important rule is that "Total Processors = nproc_x * nproc_y".  
* In the above example, WRF by default split the total processors (100) evenly among where nproc_x=10 and nproc_y=10.  
* The problem is that each processor needs to be running at least 10 grid cells and as it stands, each processor runs 25 grid cells in the x-direction and only 6 grid cells in the y-direction.  
* Because each processor only runs 6 grid cells in the y-direction, we get an error.  So we can reduce the nproc_y value to increase how many grid cells each processor will take ownace of in the y-direction.  
* Keep in mind, that "Total Processors = nproc_x * nproc_y" and if we decrease nproc_y, we must increase nproc_x.  
* The result is that we can set "nproc_x=20" and "nproc_y=5".  
* This reduces the number of processors in the y-direction, allowing each processor to have at least 10 gridcells, while 20*5=100.  
* ![image](https://github.com/user-attachments/assets/812f236c-0805-4fe1-9594-0a25d052b8df).  
-->

# Efficient WRF Simulation and Domain Decomposition

Running a WRF simulation is straightforward, but doing it **efficiently**—especially when simulating dust transport from Africa to Puerto Rico or other parts of the Americas—is much more complex. These long-distance domains are often **rectangular**, rather than square (which WRF prefers).

## Why Processor Decomposition Matters

Sometimes your domain will be an odd shape or you need more processors than the default WRF formula allows (such as if you were running chemistry).  
If you choose a high number of processors and are met with a `"the domain size is too small for this many processors, or the decomposition aspect ratio is poor"` error, `nproc_x` and `nproc_y` are possible solutions.

If you simply select `16` processors, WRF will usually default to a square decomposition:
```text
nproc_x = 4
nproc_y = 4   # Because 4 × 4 = 16
```
However, for **rectangular domains**, this choice is often **inefficient**. You should not blindly assign the same number of processors to X and Y directions.

---

## Example Domain Setup

```fortran
&domains
 max_dom = 3
 e_we    = 221, 65, 57
 e_sn    = 61,  45, 37
```

Let’s assume you must run with a small number of processors, say **4 cores**—this would work but may not be optimal.

---

## Rules for Choosing `nproc_x` and `nproc_y`

1. **Each processor must handle at least 10 grid cells** in each direction:
   ```text
   (e_we - 1) / nproc_x ≥ 10
   (e_sn - 1) / nproc_y ≥ 10
   ```

2. **The same `nproc_x` and `nproc_y` apply to all domains.**
3. **Total Processors = nproc_x × nproc_y**

---

## Minimum Grid Sizes → Determine Max Processors

From the third domain:
- `e_we = 57 → 56 cells → 56 / 10 ≈ 5 → nproc_x ≤ 5`
- `e_sn = 37 → 36 cells → 36 / 10 ≈ 3 → nproc_y ≤ 3`

So the safest **maximum** decomposition is:
```text
nproc_x = 5
nproc_y = 3
```
This setup uses `5 × 3 = 15 processors`, which respects the rules above.

---

## Common Error and Its Solution

![Error Example](https://github.com/user-attachments/assets/57a513a8-1943-4b5f-9380-8c29bb6786c5)

This error was thrown for a rectangular domain that needed at least 100 processors to run in a reasonable time frame.  
WRF by default split the total processors (100) evenly:
```text
nproc_x = 10
nproc_y = 10
```
This made each processor handle only 6 grid cells in the y-direction (below the required 10), causing the error.

**Solution:** set
```text
nproc_x = 20
nproc_y = 5
```
This ensures each processor gets enough grid cells in both directions:
![Corrected Setup](https://github.com/user-attachments/assets/812f236c-0805-4fe1-9594-0a25d052b8df)

---

## Enhancing Efficiency: Adjust Domain Dimensions

You can slightly modify the domains to allow **better parallelism**:

```fortran
&domains
 max_dom = 3
 e_we    = 221, 65, 60
 e_sn    = 61,  45, 40
```

With these rounded values:
- `e_we = 60 → 59 cells → 59 / 6 ≈ 9.8`
- `e_sn = 40 → 39 cells → 39 / 4 ≈ 9.75`

So now you can use:
```text
nproc_x = 6
nproc_y = 4
```
→ 24 processors with better load balancing and faster simulation time.

---

## ⚠️ Important Notes

- Comment the lines `nproc_x` and `nproc_y` like this `!nproc_x = 6` in the `namelist.input` **before running `real.exe`** to avoid errors.
- After `real.exe`, uncomment them for `wrf.exe`.

Also, your SLURM scripts for `real.exe` and `wrf.exe` must request **the same number of processors**.

### For Real
```bash
#SBATCH -N 1    
#SBATCH -n 20   
srun -N1 -n15 ./real.exe > real.log 2>&1
```

### For WRF
```bash
#SBATCH -N 1                           
#SBATCH -n 20                          
srun -N1 -n15 ./wrf.exe > wrf.log 2>&1
```

---

## ✅ Summary

- Always analyze **grid size** before choosing processor count.
- Ensure `(e_we - 1) % nproc_x == 0` and `(e_sn - 1) % nproc_y == 0`.
- Each processor should handle **at least 10×10 cells**.
- For rectangular domains → **asymmetric decomposition**.
- Adjust domain dimensions when possible.
- Efficient processor decomposition improves performance and avoids runtime errors.

# Problems of SST of 0 values on the met_em files
"If you are planning to run simulations that go out for more than about a week, it's advised to use an outside source for SST data. Most datasets (for e.g., GFS) typically come with an SST field, but they are usually coarse and not reliable for an extended time. If you are not doing long simulations, then it's okay to skip the outside SST source. In that case, you don't even need to specify anything extra in the namelist.input file - so you don't need to add sst_update, and it's corresponding settings." 

If you need more information of how to do this, refeer to the file `Running WRF with ERA5.pptx`

![image](https://github.com/user-attachments/assets/c10a61a1-b3ee-462f-8a8d-1e4ad836392a)

Source [Link](https://forum.mmm.ucar.edu/threads/re-enquiry-about-sst-update-in-wrf.8113/)

# If you delete your Vtable

If you erase the Vtable here you can find a fast copy

## For GFS
[GFS Vtable](https://github.com/yyr/wps/blob/master/ungrib/Variable_Tables/Vtable.GFS)

## For ECMWF
[ECMWF Vtable](https://github.com/yyr/wps/blob/master/ungrib/Variable_Tables/Vtable.ECMWF)

## Other Vtables
[Other Vtables](https://github.com/yyr/wps/tree/master/ungrib/Variable_Tables)



# Send a process after another on the cluster

You can execute a script on the cluster and automatically launch another one as soon as the first job finishes successfully. This is particularly useful, for example, when you need to run the `real.exe` step first and then start `wrf.exe`.

```sh
## Launch the first REAL job
cd "${local_data_dir_feedback}feedback_0" || { echo "Failed to change directory to ${local_data_dir_feedback}feedback_0"; exit 1; }
jobid_r0=$(sbatch "$local_data_dir_feedback/feedback_0/send_real.sh" | awk '{print $4}')
echo "Job ID for feedback_0: $jobid_r0"

## Submit both WRF jobs, depending on REAL jobs finishing successfully

cd "${local_data_dir_feedback}feedback_0" || { echo "Failed to change directory to ${local_data_dir_feedback}feedback_0"; exit 1; }
sbatch --dependency=afterok:$jobid_r0 "$local_data_dir_feedback/feedback_0/send_wrf.sh"
echo "Job ID for feedback_0 WRF: $jobid_r0"
```



