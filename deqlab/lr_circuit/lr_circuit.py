import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp


def dIdt(t, I, V0, R, L):
    return (V0 - R * I)/L

def dIdt_nl(t, I, V0, R0, L, m):
    return (V0 - (R0 + m * I) * I)/L

def exp_fit(t, A, la):
    return A * (1 - np.exp(-la * t))


st.title('LR Circuit')
st.header('Numerical simulation of the making current')
st.subheader('Parameters')

col1, col2 = st.columns(2)

with col1:
    V0 = st.number_input('Voltage V0:', value=12., step=0.5)
    R0 = st.number_input('Resistance R0:', value=1000, step=100, min_value=100)
    m = st.number_input('Resistance parameter m:', value=10000, step=1000)
    L = st.number_input('Inductance L:', value=10e-3, step=1e-3, min_value=0.)

with col2:
    N = st.number_input('Number of points:', value=10, min_value=5, max_value=1000000)
    model = st.selectbox('Model:', ('linear', 'nonlinear'))
    method = st.selectbox('Method:', ('Euler', 'RK45'))


# V0 = 12
# R0 = 1500
# m = 1e4
# L = 10e-3

tau = L/R0
tmax = 5*tau

dt = tmax/N

t = np.linspace(0, tmax, N)
It = np.zeros(N)

It[0] = 0


if method == 'Euler':
    for i in range(1, N):
        if model == 'linear':
            It[i] = It[i-1] + dIdt(t[i-1], It[i-1], V0=V0, R=R0, L=L) * dt
        elif model == 'nonlinear':
            It[i] = It[i-1] + dIdt_nl(t[i-1], It[i-1], V0=V0, R0=R0, m=m, L=L) * dt

elif method == 'RK45':
    if model == 'linear':
        sol = solve_ivp(dIdt, [0, tmax], [It[0]], t_eval=t, args=(V0, R0, L))
        It = sol.y[0]
    elif model == 'nonlinear':
        sol = solve_ivp(dIdt_nl, [0, tmax], [It[0]], t_eval=t, args=(V0, R0, L, m))
        It = sol.y[0]

fig, ax = plt.subplots()
ax.plot(t, It)

st.subheader('Graph')
st.pyplot(fig)

param, cov = curve_fit(exp_fit, t, It)

I0_fit = param[0]
tau_fit = 1/param[1]

st.subheader('Comparison')
st.text(f'model: {model}')
st.text(f'method: {method}')
st.text(f'max current: theoretical {V0/R0*1000:.3f} mA, fit {I0_fit*1000:.3f} mA')
st.text(f'time constant: theoretical {L/R0*1e6:.3f} µs, fit {tau_fit*1e6:.3f} µs')