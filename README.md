# Stationary Data Extractor

Takes pickled data in the needed format, and removes all data that corresponds to segments where movement is less than a certain threshold, by default 10 m/s. Results placed in folder with same base name as input file, folder contains each continuous length of data that meets minimum velocity threshold.

How to execute:
```
python3 filter.py [Data file in .p format]
```