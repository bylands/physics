import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def F(q1, q2):
    rvec = np.array(q2[0]) - np.array(q1[0])
    r = sqrt(rvec.dot(rvec))
    force = 8.9875517923e9 * q1[1] * q2[1]/(r*r) * rvec/r
    return force

Qpos = [[-1, 0], [1, 0]]
Qval = [-1e-6, -2e-6]

qpos = [1-sqrt(2)*2/(1+sqrt(2)), 1]
# qpos = [0, 0]
qval = 1e-9

xrange = tuple([p[0]*1.2 for p in Qpos])
yrange = xrange

vecs = [F([Qpos[i], Qval[i]], [qpos, qval]) for i in range(len(Qpos))]
vec_res = sum(vecs)

plt.xlim(xrange)
plt.ylim(yrange)
axes=plt.gca()
axes.set_aspect(1)

for vec in vecs:
    plt.quiver(qpos[0], qpos[1], vec[0], vec[1], angles='xy', scale_units='xy', scale=2e-5)
    
plt.quiver(qpos[0], qpos[1], vec_res[0], vec_res[1], color='g', angles='xy', scale_units='xy', scale=2e-5)

for c in [plt.Circle(tuple(pos), 0.1) for pos in Qpos]:
    plt.gca().add_patch(c)

plt.gca().add_patch(plt.Circle(tuple(qpos), 0.05, fc='red'))

# plt.grid()
plt.show()