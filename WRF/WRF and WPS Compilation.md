# Introduction
This is a written account of my attempt to compile WRF4.2 as of 1/22/2025.  
This follows the official WRF tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php), but also includes photos and any tips or troubles I run into.  
Important Note: I am compiling this on a system that has all of the necessary libraries such as GNU gcc and foretran already installed.  

# Tars
The first step is to prepare your tars and get your files in order.  
To get the WRF compilation tar, you can visit [THIS](https://github.com/wrf-model/WRF/releases) github.  
* Make a new directory called "build-wrf".
* "cd" into the "build-wrf" directory and make a new directory called "wrf_tars".
* "cd" into "build-wrf/wrf_tars" and download the [WRF](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz) and [WPS](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz) tars using "wget".
![image](https://github.com/user-attachments/assets/065b83a3-8a58-4bf6-bc40-fa77cef199f8).


# System Environment Tests
The Second step is to makesure your gfortran, cpp, and gcc are working.  
If you're compiling these on LSU's systems then these should work without any issue. 
* type "which gfortran".  
* type "which cpp".  
* type "which gcc".  
If there is a version on the system then the above commands will identify the path to each.
![image](https://github.com/user-attachments/assets/2e367f42-3a35-4da2-bc11-3726fdcc3f82).  

&nbsp;

* Within the "build_wrf" directory, create a new directory called "tests".
* "cd" into the new "tests" directory.
* use "wget" to download the Fortran and C Tests from [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_tests.tar).  
![image](https://github.com/user-attachments/assets/1941f32d-4dd2-4af8-8f26-b7e9ae678f23).
* Unpack the tar file with "tar -xf Fortran_C_tests.tar".
There are Seven tests that will be run.  Each is a subheading below.  
### Test #1
* Type "gfortran TEST_1_fortran_only_fixed.f".
* Type "./a.out".
* The following should be outputted: "SUCCESS test 1 fortran only fixed format".
### Test #2
* Type "gfortran TEST_2_fortran_only_free.f90".
* Type "./a.out".
* The following should be outputted: "Assume Fortran 2003: has FLUSH, ALLOCATABLE, derived type, and ISO C Binding
SUCCESS test 2 fortran only free format".  
### Test #3
* Type "gcc TEST_3_c_only.c".
* Type "./a.out".
* The Following should be outputted: "SUCCESS test 3 C only".
### Test #4






