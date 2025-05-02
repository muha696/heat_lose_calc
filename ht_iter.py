from heat_lose import HeatLoses
import numpy as np

def f(tin, tou):
    result = HeatLoses(dn=630, su=12, tin=tin, tou=tou, tgr=5, lamizp=0.033, lamizo=0.033, lamgr=1.92)
    return result.calc_los()

def tou_find(tin, qpr, qob, gkal):
    vatt = gkal * 1163000
    l = 1500
    Q = qpr * l
    G = 500 / 3.6
    delta_t = Q * 0.001 / (G * 4.185)
    tin_con = tin - delta_t
    delta_tou = vatt * 0.001 / (G * 4.185)
    tou = tin_con - delta_tou
    Qob = qob * l
    delta_tob = Qob * 0.001 / (G * 4.185)
    tob = tou + delta_tob
    return tob

tin = 90

q = f(tin, 50)
tou = tou_find(tin, q[1], q[2], 25)
qx = f(tin, tou)
while np.abs(q[0] - qx[0]) >= 0.001:
    print(q[0], qx[0], np.abs(q[0] - qx[0]) / q[0], tou, tin)
    q = qx
    tou = tou_find(90, q[1], q[2], 20)
    qx = f(90, tou)













