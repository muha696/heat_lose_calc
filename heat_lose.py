import numpy as np
import matplotlib.pyplot as plt

stb_trubes = {

     'DN': [133, 159, 165, 219, 273, 325, 377, 426, 530, 630, 720],
     'DOUT': [225, 250, 250, 315, 400, 450, 500, 560, 710, 800, 900],

}

tkp_trubes = {'DN': [32.0, 33.5, 38.0, 42.3, 45.0, 48.0, 57.0, 60.0,
                     75.5, 76.0, 88.5, 89.0, 108.0, 114.0, 133.0, 140.0,
                     159.0, 165.0, 219.0, 273.0, 325.0, 377.0, 426.0, 530.0,
                     630.0, 720.0, 820.0, 920.0, 1020.0],
              'Глубина': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                          1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                          1.0, 1.0, 1.0, 1.1, 1.1, 1.2, 1.3, 1.3, 1.3],
              'Расстояние': [0.24, 0.24, 0.26, 0.26, 0.26, 0.26, 0.275, 0.275,
                             0.29, 0.29, 0.31, 0.31, 0.35, 0.35, 0.375, 0.375,
                             0.5, 0.5, 0.565, 0.65, 0.7, 0.75, 0.81, 0.96, 1.05,
                             1.25, 1.35, 1.45, 1.55],

              'Поток О': [8.4, 8.7, 8.2, 9.0, 9.6, 10.3, 10.7, 11.4, 13.4, 13.5,
                          13.9, 14.0, 13.5, 14.6, 15.5, 17.0, 18.1, 19.5, 22.2,
                          21.6, 25.0, 28.5, 29.7, 28.5, 34.6, 37.2, 41.3, 46.1, 51.0],

              'Поток Б': [16.6, 17.4, 16.2, 17.9, 19.1, 20.6, 21.6, 23.0, 27.4, 27.6,
                          28.3, 28.6, 27.2, 29.7, 31.7, 35.0, 36.9, 40.0, 45.8, 44.0,
                          51.2, 59.0, 61.3, 58.2, 71.4, 76.7, 86.1, 96.7, 107.2],

              'Сумм поток': [25.0, 26.1, 24.4, 26.9, 28.7, 30.9, 32.3, 34.4, 40.8, 41.1,
                             42.2, 42.6, 40.7, 44.3, 47.2, 52.0, 55.0, 59.5, 68.0, 65.6,
                             76.2, 87.5, 91.0, 86.7, 106.0, 113.9, 127.4, 142.8, 158.2]}


class HeatLoses:
    def __init__(self, dn, su, tin, tou, tgr, lamizp, lamizo, lamgr = None):
        self.su = su
        self.tin = tin
        self.tou = tou
        self.tgr = tgr
        self.lamizp = lamizp
        self.lamizo = lamizo
        self.lamgr = 1.92 if lamgr is None else lamgr
        self.dn = dn
        self.id_trube_stb = stb_trubes['DN'].index(self.dn)
        self.id_trube_tkp = tkp_trubes['DN'].index(self.dn)
        self.hin = tkp_trubes['Глубина'][self.id_trube_tkp]
        self.b = tkp_trubes['Расстояние'][self.id_trube_tkp]
        self.dout = stb_trubes['DOUT'][self.id_trube_stb]
        self.diz = self.dout - 2 * self.su

    def res_ground(self):
        r1 = (1/(2*np.pi*self.lamgr))
        r2 = np.log((2*(self.hin)/(0.001*self.dout)) + np.sqrt((2*(self.hin)/(0.001*self.dout))*(2*(self.hin)/(0.001*self.dout)) - 1))
        R = r1*r2
        return R

    def restrube(self, lamiz):
        Ris = (1/(2*np.pi*lamiz)) * np.log((self.diz)/self.dn)
        Rsu = (1/(2*np.pi*0.42)) * np.log((self.dout)/self.diz)
        R = Ris + Rsu
        return R

    def calc_los(self):
        R1 = self.restrube(self.lamizp) + self.res_ground()
        R2 = self.restrube(self.lamizp) + self.res_ground()
        R0 = (1/(2*np.pi*self.lamgr)) * np.log(np.sqrt(1 + (2*self.hin/self.b)**2))
        q1 = ((self.tin - self.tgr) * R2 - (self.tou - self.tgr) * R0) / (R1*R2 - R0*R0)
        q2 = ((self.tou - self.tgr) * R1 - (self.tin - self.tgr) * R0) / (R1 * R2 - R0 * R0)
        q = q1 + q2
        return q, q1, q2