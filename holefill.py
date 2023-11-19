import pickle
import sys
import os
import torch
import numpy as np

filepath = sys.argv[1]
data = pickle.load(open(filepath, "rb"))

elems = len(data['p'])
name = filepath[len(filepath) - filepath[::-1].index('/'):
    len(filepath) - filepath[::-1].index('.') - 1]

new_p = data['p']

i = 1
maxCounter = sys.float_info.min
timeOfMax = 0
while i < elems:
    counter = 0
    while data['p'][i + counter] == data['p'][i - 1]:
        counter += 1

    step = np.array(data['p'][i + counter]) - np.array(data['p'][i - 1]) / (counter + 1)

    for j in range(0, counter):
        new_p_i = list(np.array(data['p'][i - 1]) + step * (j + 1))
        new_p[i + j] = new_p_i
    
    i += counter + 1

data['p'] = new_p
data['name'] = name + '_filled'

dmp = open(os.path.join('./', data["name"] + ".p"), "wb")
pickle.dump(data, dmp)


