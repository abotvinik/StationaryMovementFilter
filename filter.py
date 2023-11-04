import pickle
import sys
import os
import torch
import numpy as np

filepath = sys.argv[1]
name = filepath[len(filepath) - filepath[::-1].index('/'):
    len(filepath) - filepath[::-1].index('.') - 1]
path = os.path.join('./', name + '_filtered')
if not os.path.exists(path): os.mkdir(path)

data = pickle.load(open(filepath, "rb"))

elems = data['u'].shape[0]

init_ang_gt = data['ang_gt'].cpu().detach().numpy()
init_p_gt = data['p_gt'].cpu().detach().numpy()
init_t = data['t'].cpu().detach().numpy()
init_v_gt = data['v_gt'].cpu().detach().numpy()
init_u = data['u'].cpu().detach().numpy()
init_quat_test = data['quat_test'].cpu().detach().numpy()
init_t0 = data['t0']

count = 0

ang_gt = []
p_gt = []
t = []
v_gt = []
u = []
quat_test = []

for i in range(0, elems):
    print(i, end='\r')

    if len(ang_gt) == 0 and np.linalg.norm(init_v_gt[i]) < 10:
        continue

    if len(ang_gt) < 100 and np.linalg.norm(init_v_gt[i]) < 10:
        ang_gt = []
        p_gt = []
        t = []
        v_gt = []
        u = []
        quat_test = []
        continue

    if np.linalg.norm(init_v_gt[i]) < 10:
        print('New list terminating')
        t0 = init_t0 + t[0]
        t = t - t[0]

        d = {'name': name, 'ang_gt': ang_gt, 'p_gt': p_gt, 't': t.tolist(), 't0': t0, 'v_gt': v_gt, 'u': u, 'quat_test': quat_test}
        print('Dictionary Made')

        for key in d:
            if isinstance(d[key], list):
                print('Converting ' + key + ' to FloatTensor')
                d[key] = torch.FloatTensor(d[key])
            print(type(d[key]))

        dmp = open(os.path.join('./' + name + '_filtered/', d["name"] + "_set_" + str(count) + ".p"), "wb")
        pickle.dump(d, dmp)
        count += 1
        ang_gt = []
        p_gt = []
        t = []
        v_gt = []
        u = []
        quat_test = []
        continue

    ang_gt.append(init_ang_gt[i])
    p_gt.append(init_p_gt[i])
    t.append(init_t[i])
    v_gt.append(init_v_gt[i])
    u.append(init_u[i])
    quat_test.append(init_quat_test[i])

if len(ang_gt) > 100:
    d = {'name': name, 'ang_gt': ang_gt, 'p_gt': p_gt, 't': t, 't0': t0, 'v_gt': v_gt, 'u': u, 'quat_test': quat_test}

    for key in d:
        if isinstance(d[key], list):
            d[key] = torch.FloatTensor(d[key])

    dmp = open(os.path.join('./' + name + '_filtered/', d["name"] + "_set_" + str(count) + ".p"), "wb")
    pickle.dump(d, dmp)