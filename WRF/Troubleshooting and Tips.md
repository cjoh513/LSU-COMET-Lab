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
### Adding to configure.wrf
* 




