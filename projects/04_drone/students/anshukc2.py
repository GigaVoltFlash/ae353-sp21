import numpy as np
from scipy import linalg
class RobotController:
    def __init__(self, limiter=None):
        self.dt = 0.01
        self.limiter = limiter
        self.A = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, 0.0, 1.0],
 [0.0, 0.0, 0.0, 0.0, 9.81, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, -9.81, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, -0.0, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        self.B = np.array([[0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, 0.0],
 [0.0, 0.0, 0.0, -0.0],
 [0.0, 0.0, 0.0, 2.0],
 [434.7826086956522, 0.0, 0.0, 0.0],
 [0.0, 434.7826086956522, 0.0, 0.0],
 [0.0, 0.0, 250.0, 0.0]])
        self.C = np.array([[1,0,0,0,0,0,0,0,0,0,0,0],
              [0,1,0,0,0,0,0,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0,0,0,0],
              [0,0,0,0,0,1,0,0,0,0,0,0]])
        self.K = np.array([[-7.470103824860964e-16,
  -0.597614304667193,
  -2.534736450492715e-16,
  2.131279246713305,
  -2.2795088647501232e-15,
  1.2174213473461131e-14,
  -5.725766455299804e-16,
  -0.6115194547658369,
  2.1235858790732371e-16,
  0.3522635360360125,
  1.882304521121369e-17,
  9.777282575744851e-17],
 [0.26726124191242473,
  -2.9636468334901435e-17,
  3.3383667491262037e-16,
  -4.687289900146584e-16,
  1.7324268494946549,
  4.0340005770852824e-17,
  0.3892794424612655,
  4.4031235194257394e-16,
  3.996567687509206e-18,
  1.882304521121369e-17,
  0.3496496500690224,
  -3.7084882309639604e-17],
 [-2.4083942781012557e-16,
  -9.452569554399674e-15,
  -1.6235935707886185e-16,
  9.560492828896679e-15,
  7.267272416605851e-16,
  0.5855400437691188,
  1.0873236001454141e-16,
  -3.634259171884253e-15,
  -9.553253349797393e-17,
  5.621937481053289e-17,
  -2.1323807328042768e-17,
  0.34492033085318],
 [-8.423703219100551e-17,
  -1.1812055222399395e-15,
  1.581138830084189,
  1.754554067453382e-15,
  -7.341405092272812e-16,
  -7.782195460359621e-16,
  -2.3199499377039327e-16,
  -1.0143593903012036e-15,
  1.8923897141139292,
  3.418973265307912e-17,
  6.434473976889822e-19,
  -2.6749109379432702e-17]])
        self.L = np.array(
[[11.3058803110068, 0.0, 0.0, 0.0, 0.4396776833728971, 0.0],
 [0.0, 11.3058803110068, 0.0, -0.4396776833728971, 0.0, 0.0],
 [0.0, 0.0, 10.954451150103324, 0.0, 0.0, 0.0],
 [0.0, -0.4396776833728971, 0.0, 10.945603950560619, 0.0, 0.0],
 [0.4396776833728971, 0.0, 0.0, 0.0, 10.945603950560619, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 10.954451150103324],
 [14.00812303603352, 0.0, 0.0, 0.0, 9.717323102417483, 0.0],
 [0.0, 14.00812303603352, 0.0, -9.717323102417483, 0.0, 0.0],
 [0.0, 0.0, 10.0, 0.0, 0.0, 0.0],
 [0.0, -0.06615794931719185, 0.0, 9.999781153892402, 0.0, 0.0],
 [0.06615794931719185, 0.0, 0.0, 0.0, 9.999781153892402, 0.0],
 [0.0, 0.0, 0.0, 0.0, 0.0, 10.0]])
        self.f_z_e = 9.81/2
    def get_color(self):
        return [1., 0., 0.]

    def reset(self, pos):
        self.xhat = np.array([[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.]])
        self.time = 0.


    def run(self, pos, rpy, pos_ring, is_last_ring, pos_others):
        offset = -0.4 # The offset to prevent collisions with the ring
        y = np.array([[pos[0]], [pos[1]], [pos[2]], [rpy[0]], [rpy[1]], [rpy[2]]]) #Sensor data
        dist = linalg.norm([[pos_ring[0] + offset - pos[0]], [pos_ring[1] - pos[1]], [pos_ring[2] - pos[2]]]) #Distance between current and desired
        displace_vec = ([[pos_ring[0] + offset - pos[0]], [pos_ring[1] - pos[1]], [pos_ring[2] - pos[2]]])/dist #Unit displacement vector
        if dist < 1.:
            v_vect = np.array([[1.2], [0.], [0.]]) #That push through the hoop
        else:
            v_vect = displace_vec * (dist)**2 * 0.06 #Variable velocity vector
    
        x_des = np.array([[pos_ring[0] + offset],[pos_ring[1]],[pos_ring[2]],[0.],[0.],[0.],[v_vect[0,0]],[v_vect[1,0]],[v_vect[2,0]],[0.],[0.],[0.]]) # Setting the desired state
        if is_last_ring:
            x_des[2,0] += 0.4 #To ensure that it doesn't hit the wall of the ending ring

        if self.time < 15:
            x_des = np.array([[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.]])
        max_error = 1.4 #error control

        for i in range(12):
            if np.abs(x_des[i,0] - self.xhat[i,0]) > max_error:
                x_des[i,0] = self.xhat[i,0] + max_error * ((x_des[i,0] - self.xhat[i,0]) / linalg.norm(x_des[i,0] - self.xhat[i,0]))

        u = -self.K @ (self.xhat - x_des)
        tau_x = u[0,0]
        tau_y = u[1,0]
        tau_z = u[2,0]
        if y[2,0] <= 0.5:
            u[3,0] = 2.5
        if is_last_ring: #Turning off upward force to make the drone fall into the ring
            if abs(pos_ring[0] - pos[0]) < 0.6 and abs(pos_ring[1] - pos[1]) < 0.6:
                u[3,0] = -100.

        f_z = u[3,0] + self.f_z_e
        if self.limiter is not None:
            tau_x, tau_y, tau_z, f_z = self.limiter(tau_x, tau_y, tau_z, f_z)
        u[3,0] = f_z - self.f_z_e
        self.xhat += self.dt * (self.A @ self.xhat + self.B @ u - self.L @ (self.C @ self.xhat - y)) #State estimation
        self.time += self.dt

        return tau_x, tau_y, tau_z, f_z