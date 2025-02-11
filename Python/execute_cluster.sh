#!/bin/bash                                                                          
#SBATCH -p single                                                                    
#SBATCH --time=01:00:00             # Time limit (hh:mm:ss)                          
#SBATCH -N 1                                                                         
#SBATCH -n 2                                                                         
#SBATCH -J testETM                                                                   
#SBATCH --mail-type=END,FAIL        # Notifications for job done & fail              
#SBATCH --mail-user=[YourEmail]@lsu.edu # Send notifications to this email               
#SBATCH -A [YourAllocation]            # Allocation name (req'd if you have more than 1)
#SBATCH --output=output_%j.txt      # Output file (with job ID in the name)          
#SBATCH --error=error_%j.txt        # Error file (with job ID in the name)           
                                                                                     
                                                                                     
# Check if a Python script is provided as an argument                                
if [ -z "$1" ]; then                                                                 
    echo "Usage: sbatch execute_cluster.sh <python_script>"                          
    exit 1                                                                           
fi                                                                                   
                                                                                     
PYTHON_SCRIPT=$1                                                                     
                                                                                     
# Load the conda module                                                              
source ~/miniconda3/etc/profile.d/conda.sh                                           
conda activate wrf-py                                                                
                                                                                     
# Run the specified Python script and save output to outputs.txt                     
python "$PYTHON_SCRIPT" > outputs_${SLURM_JOB_ID}.txt 2>&1                           
                                                                                     
# To run this script, use the following command:                                     
# sbatch execute_cluster.sh cross_section/create_graph.py                            
