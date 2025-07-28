# Adjustable parameters
params = {
    "mass_upper": 60.0,
    "mass_lower": 5.0,
    "spring_k": 12000.0,
    "spring_rest_length": 1.0,
    "damping": 300.0,
    "gravity": 9.81,
    "initial_y": 1.1,
    "initial_x": 0.0,            # NEW: initial horizontal position
    "initial_vy": -1.0,
    "initial_vx": 2.5,           # NEW: horizontal velocity [m/s]
    "leg_length": 1.0,
    "stride_duration": 0.4,      # NEW: stride period (s)
    "time_step": 0.01,
    "total_time": 3.0
}