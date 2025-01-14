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
* 







