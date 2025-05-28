## Information related to Python scripts we use frequently.  Below is a brief description for what each file in this directory contains
### LSU HPC Python sbatch Submission
* The basic steps for using LSU's HPC supermic to submit a batch job that incorporates Python

### netcdf_plotting_functions.py
* A Python script that contains many useful functions related to extracting and plotting variables within netCDFs
### wrfout_plotting_functions.py
* A python script containing many useful functions related to extracting and plotting variables within wrfout files specifically.

## Execute a python code from the cluster
If you need to execute a python code you can use the code called `executed_cluster.sh` which use in a optimal way the resources to run a python code. The way to execute is like this.

```sh
sbatch execute_cluster.sh [code_of_python].py
```

Real example
```sh
sbatch execute_cluster.sh cross_section/create_graph.py
```
