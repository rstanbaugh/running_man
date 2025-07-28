import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate(x, y, leg_contact, params):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(0, np.max(x) + 1)
    ax.set_ylim(0, 2)

    body_line, = ax.plot([], [], 'o-', lw=3)  # torso to stance foot
    swing_line, = ax.plot([], [], 'o--', lw=2)  # torso to swing leg

    def init():
        body_line.set_data([], [])
        swing_line.set_data([], [])
        return body_line, swing_line

    def update(i):
        torso = (x[i], y[i])
        foot_y = 0
        stride_len = 0.5  # fixed swing leg arc

        # Determine stance and swing foot positions
        if leg_contact[i]:
            stance_foot = (x[i], foot_y)
            swing_foot = (x[i] + stride_len, foot_y)
        else:
            stance_foot = (x[i] - stride_len, foot_y)
            swing_foot = (x[i], foot_y)

        # Update torso to stance foot
        body_line.set_data([stance_foot[0], torso[0]], [stance_foot[1], torso[1]])

        # Update torso to swing foot (dashed line)
        swing_line.set_data([torso[0], swing_foot[0]], [torso[1], swing_foot[1]])

        return body_line, swing_line

    ani = animation.FuncAnimation(fig, update, frames=len(x),
                                  init_func=init, blit=True, interval=20)
    plt.title("Hybrid Running Model with Horizontal Motion and Swing Leg")
    plt.xlabel("Horizontal Position (m)")
    plt.ylabel("Vertical Position (m)")
    plt.show()