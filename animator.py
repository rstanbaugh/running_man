import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate(y, params):
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 2)
    line, = ax.plot([], [], lw=3, marker='o')

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        # Foot fixed at ground (0, 0)
        foot = (0, 0)
        torso = (0, y[frame])
        line.set_data([foot[0], torso[0]], [foot[1], torso[1]])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(y),
                                  init_func=init, blit=True, interval=20)
    plt.xlabel("Lateral position (m)")
    plt.ylabel("Vertical position (m)")
    plt.title("Hybrid Running Model - SLIP + Two-Mass (Simplified)")
    plt.show()