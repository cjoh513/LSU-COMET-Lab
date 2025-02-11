## Execute a python code from the cluster
If you need to execute a python code you can use the code called `executed_cluster.sh` which use in a optimal way the resources to run a python code. The way to execute is like this.

```sh
sbatch execute_cluster.sh [code_of_python].py
```

Real example
```sh
sbatch execute_cluster.sh cross_section/create_graph.py
```
