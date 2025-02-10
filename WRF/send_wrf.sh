#!/bin/bash
#SBATCH -N 1                            ### Big job, 1-year sim over the entire USA. Each Node can use up to 20 tasks
#SBATCH -n 20                           ### The way I found it to work is to ask for the number of nodes then the total processors/tasks.  so each node can use up to 20 tasks so I ask for 10 nodes and 200 tasks as 20*10=200
#SBATCH -t 70:00:00                      ### 72 hours was the max wall time usable.  
#SBATCH -p workq                         ### workq lets you use multiple nodes, which means you need to specify the number of tasks you want.
#SBATCH -J feed0
#SBATCH -A [ChargedCOUNT!!!! like hpc_@#$%^&*]                 ### The charged acccount.  As said in the "sub_copy_wrf" file, you can probably use this one if you've got access to it, otherwise you'll have to talk to Paul to get access
#SBATCH --mail-user [YourEMAIL!!!!!!!!!]@lsu.edu      ### The email it sends notifications to related to the batch
#SBATCH --mail-type FAIL,END             ### Under what conditions it sends emails to you
#SBATCH --output=output_%j.txt      # Output file (with job ID in the name)
#SBATCH --error=error_%j.txt        # Error file (with job ID in the name)



#This one is just to run wrf.exe so I move to the proper direectory and have it execute it with the 200 processors I requested

# Source the environment variables
source /work/etorresm/wrf/Build_WRF/var_env.sh

# Execute WRF with the requested resources
srun -N1 -n20 ./wrf.exe
