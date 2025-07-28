# simulation + energy

import numpy as np

def simulate(params):
    dt = params["dt"]
    steps = int(params["total_time"] / dt)
    
    x = np.zeros(steps)
    y = np.zeros(steps)
    vx = np.zeros(steps)
    vy = np.zeros(steps)
    ke = np.zeros(steps)
    pe = np.zeros(steps)

    x[0] = params["initial_x"]
    y[0] = params["initial_y"]
    vx[0] = params["initial_vx"]
    vy[0] = params["initial_vy"]

    for i in range(1, steps):
        force_y = -params["mass"] * params["gravity"]

        spring_extension = max(0.0, params["spring_rest_length"] - y[i-1])
        spring_force = params["spring_k"] * spring_extension

        if y[i-1] <= params["spring_rest_length"]:
            force_y += spring_force

        ay = force_y / params["mass"]
        vy[i] = vy[i-1] + ay * dt
        y[i] = y[i-1] + vy[i] * dt

        x[i] = x[i-1] + vx[i-1] * dt
        vx[i] = vx[i-1]  # constant horizontal speed

        ke[i] = 0.5 * params["mass"] * (vx[i] ** 2 + vy[i] ** 2)
        pe[i] = params["mass"] * params["gravity"] * y[i]

    return x, y, vx, vy, ke, pe
