# Stationary Data Extractor

Takes pickled data in the needed format, and removes all data that corresponds to segments where movement is less than a certain threshold. Results placed in folder with same base name as input file, folder contains each continuous length of data that meets minimum velocity threshold.

Change the threshold velocity using the global `THRESHOLD_VELOCITY` variable

How to execute:
```
python3 filter.py ./[Data file in .p format]
```

Input data file is expected to have a dictionary with the following contents:

`'name'`: Name of respective rosbag

`'r'`: Rotation

`'v'`: Velocity

`'p'`: Position

`'u'`: State vector ([$a_x$, $a_y$, $a_z$, $\omega_x$, $\omega_y$, $\omega_z$])

`'t'`: Time