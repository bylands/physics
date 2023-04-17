import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

'''
Find the trajectory of a charged particle in a combined electric and magnetic field
'''

# define fields

Ex, Ey, Ez = (-1e2, 0, 0) # electric field in V/m

Bx, By, Bz = (-1e-4, 0, 0) # magnetic field in T


# define particle

q = -1.602e-19 # elementary charge in C
m = 9.109e-31 # mass of an electron in kg

x0, y0, z0 = (0, 0, 0) # initial position in m
v0x, v0y, v0z = (0, 3e6, 0) # initial velocity in m/s
init = [x0, y0, z0, v0x, v0y, v0z] # initial conditions


# force calculation

def force(q, vx, vy, vz, Ex, Ey, Ez, Bx, By, Bz):
    
    FEx, FEy, FEz = q*Ex, q*Ey, q*Ez
    FBx = q*(vy*Bz-vz*By)
    FBy = q*(vz*Bx-vx*Bz)
    FBz = q*(vx*By-vy*Bx)

    return (FEx+FBx, FEy+FBy, FEz+FBz)


# define differential equation

def S(time, r, q, m, Ex, Ey, Ez, Bx, By, Bz):
    
    x, y, z, vx, vy, vz = r
    Fx, Fy, Fz = force(q, vx, vy, vz, Ex, Ey, Ez, Bx, By, Bz)
    ax, ay, az = (Fx/m, Fy/m, Fz/m)
    return [vx, vy, vz, ax, ay, az]


# solve differential equation

tmax = 2e-6 # max time for simulation
N = 10000 # number of points for simulation
t = np.linspace(0, tmax, N) # times for evaluation

args = (q, m, Ex, Ey, Ez, Bx, By, Bz)
sol = solve_ivp(S, [0, tmax], init, args=args, t_eval=t)

xs, ys, zs, vxs, vys, vzs = sol.y

# plot solution in 3d plot

plt.style.use(['seaborn-bright'])
ax = plt.figure().add_subplot(projection='3d')
ax.plot(xs, ys, zs)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.show()