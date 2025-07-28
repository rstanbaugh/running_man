import numpy as np

def simulate(params):
    dt = params["time_step"]
    T = params["total_time"]
    steps = int(T / dt)

    # Initialize arrays
    y = np.zeros(steps)
    v = np.zeros(steps)
    leg_force = np.zeros(steps)

    y[0] = params["initial_y"]
    v[0] = params["initial_vy"]

    for i in range(1, steps):
        spring_extension = params["spring_rest_length"] - y[i-1]
        F_spring = params["spring_k"] * max(0, spring_extension)
        F_damp = -params["damping"] * v[i-1]
        F_total = F_spring + F_damp - params["mass_upper"] * params["gravity"]

        # Euler integration
        a = F_total / params["mass_upper"]
        v[i] = v[i-1] + a * dt
        y[i] = y[i-1] + v[i] * dt
        leg_force[i] = F_spring

    return y, v, leg_force