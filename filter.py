import pickle
import sys
import os
import torch
import numpy as np

print('start')
THRESHOLD_VELOCITY = 5

filepath = sys.argv[1]
name = filepath[len(filepath) - filepath[::-1].index('/'):
    len(filepath) - filepath[::-1].index('.') - 1]
path = os.path.join('./', name + '_filtered')
if not os.path.exists(path): os.mkdir(path)

data = pickle.load(open(filepath, "rb"))

elems = len(data['u'])

init_r = data['r']
init_p = data['p']
init_t = data['t']
init_v = data['v']
init_u = data['u']
init_w = data['w']
init_s = data['s']
init_t0 = data['t0']
init_t_imu = data['t_imu']
init_t_gps = data['t_gps']
init_t_p = data['t_p']
init_t_ws = data['t_ws']
init_t_s = data['t_s']

count = 0

r = []
p = []
t = []
v = []
u = []
w = []
s = []
t_imu = []
t_gps = []
t_p = []
t_ws = []
t_s = []

def reset():
    global r, p, t, v, u, w, s, t_imu, t_gps, t_p, t_ws, t_s
    r = []
    p = []
    t = []
    v = []
    u = []
    w = []
    s = []
    t_imu = []
    t_gps = []
    t_p = []
    t_ws = []
    t_s = []

def append(i):
    global r, p, t, v, u, w, s, t_imu, t_gps, t_p, t_ws, t_s
    r.append(init_r[i])
    p.append(init_p[i])
    t.append(init_t[i])
    v.append(init_v[i])
    u.append(init_u[i])
    w.append(init_w[i])
    s.append(init_s[i])
    t_imu.append(init_t_imu[i])
    t_gps.append(init_t_gps[i])
    t_p.append(init_t_p[i])
    t_ws.append(init_t_ws[i])
    t_s.append(init_t_s[i])

def dump():
    global r, p, t, v, u, count
    print('New list terminating')
    t0 = init_t0 + t[0]
    t = np.array(t) - t[0]
    name_set = name + "_set_" + str(count)

    d = {'name': name_set, 'r': r, 'p': p, 't': t.tolist(), 't0': t0, 'v': v, 'u': u, 'w': w, 's': s, 't_imu': t_imu, 't_gps': t_gps, 't_p': t_p, 't_ws': t_ws, 't_s': t_s}
    print('Dictionary Made')

    # for key in d:
    #     if isinstance(d[key], list):
    #         print('Converting ' + key + ' to FloatTensor')
    #         d[key] = torch.FloatTensor(d[key])
    #     print(type(d[key]))

    dmp = open(os.path.join('./' + name + '_filtered/', d["name"] + ".p"), "wb")
    pickle.dump(d, dmp)
    count += 1

def filter():
    for i in range(0, elems):
        print(i, end='\r')

        if len(r) == 0 and np.linalg.norm(init_v[i]) < THRESHOLD_VELOCITY:
            continue

        if len(r) < 100 and np.linalg.norm(init_v[i]) < THRESHOLD_VELOCITY:
            reset()
            continue

        if np.linalg.norm(init_v[i]) < THRESHOLD_VELOCITY:
            dump()
            reset()
            continue

        append(i)

    if len(r) > 100:
        dump()
    
if __name__ == "__main__":
    filter()