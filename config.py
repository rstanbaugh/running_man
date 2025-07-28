# Adjustable parameters
params = {
    "mass_upper": 60.0,           # Torso mass [kg]
    "mass_lower": 5.0,            # Lower leg/foot mass [kg]
    "spring_k": 12000.0,          # Leg stiffness [N/m]
    "spring_rest_length": 1.0,    # Resting leg length [m]
    "damping": 300.0,             # Leg damping [Ns/m]
    "gravity": 9.81,              # Gravity [m/s^2]
    "initial_y": 1.1,             # Initial vertical height of torso [m]
    "initial_vy": -1.0,           # Initial downward velocity [m/s]
    "time_step": 0.01,            # Time step [s]
    "total_time": 2.0             # Simulation duration [s]
}