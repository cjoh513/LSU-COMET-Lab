
To execute

1) Edit the dates

```sh
vim run_many.sh 
```

Edit this part based on your namelist

```sh
START="2022-05-31 00:00"                  # first start time  (UTC)
END="2022-06-02 21:00"                    # last  start time  (UTC)
```

2) Edit the file name on `CONTROL_TEMPLATE.001`

```sh
vim CONTROL_TEMPLATE.001
```

Edit the location and name of your new files

```sh
@YY@ @MM@ @DD@ @HH@
1
18.21 -66.60 3000.0                #<======= Change the location
9999
0
10000.0
1
/home/cometlab/Downloads/delete/   #<======= Here
2022-05-31_rizza.BIN               #<======= Here too
./
tdump_@YYYYMMDDHH@
                                
```

2) Run to get the tdump files


```sh
bash run_many.sh
```

3) Run to made the graphs

```sh
bash run_graphs.sh (or execute.sh)
```

<img width="590" height="305" alt="image" src="https://github.com/user-attachments/assets/75ae0779-34ca-4dcc-92ba-b0596d8df0cd" />

