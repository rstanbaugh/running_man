import numpy as np

def simulate(params):
    dt = params["time_step"]
    T = params["total_time"]
    steps = int(T / dt)

    # Allocate arrays
    x = np.zeros(steps)
    y = np.zeros(steps)
    vx = np.zeros(steps)
    vy = np.zeros(steps)
    leg_contact = np.zeros(steps, dtype=bool)

    # Initialize
    x[0] = params["initial_x"]
    y[0] = params["initial_y"]
    vx[0] = params["initial_vx"]
    vy[0] = params["initial_vy"]

    stride_duration = params["stride_duration"]
    leg_down = True
    last_strike_time = 0

    for i in range(1, steps):
        t = i * dt

        # Determine if leg is in contact (simple stride cycle)
        if t - last_strike_time >= stride_duration:
            leg_down = not leg_down
            last_strike_time = t

        leg_contact[i] = leg_down

        # Compute vertical spring force only if leg is down
        spring_extension = params["spring_rest_length"] - y[i-1]
        F_spring = params["spring_k"] * max(0, spring_extension) if leg_down else 0
        F_damp = -params["damping"] * vy[i-1] if leg_down else 0
        F_total_y = F_spring + F_damp - params["mass_upper"] * params["gravity"]

        # Simple horizontal: no spring, just inertia
        ax = 0
        ay = F_total_y / params["mass_upper"]

        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt

        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt

        # Prevent torso from penetrating ground
        if y[i] < 0:
            y[i] = 0
            vy[i] = 0

    return x, y, vx, vy, leg_contact