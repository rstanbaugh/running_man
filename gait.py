# generates limb angles per frame

import numpy as np

def gait_angles(t, freq=2.0):
    w = 2 * np.pi * freq
    hip = 30 * np.sin(w * t)             # degrees
    knee = 40 * np.sin(2 * w * t + np.pi/2)
    shoulder = -hip
    elbow = 30 * np.sin(2 * w * t)
    return np.deg2rad(hip), np.deg2rad(knee), np.deg2rad(shoulder), np.deg2rad(elbow)

# animator.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from gait import gait_angles

def animate(x, y, vx, vy, ke, pe, params):
    fig, (ax_run, ax_data) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]})
    ax_run.set_xlim(-1, 1)
    ax_run.set_ylim(0, 2)
    ax_run.set_aspect('equal')
    ax_run.axis('off')

    # Background sidewalk
    bg_x = np.linspace(0, np.max(x)+2, 500)
    bg_y = 0.1 * np.sin(0.5 * bg_x) + 0.1
    bg_line, = ax_run.plot([], [], color='gray', lw=2)

    # Stickman body parts
    torso, = ax_run.plot([], [], 'k-', lw=3)
    head, = ax_run.plot([], [], 'ko', markersize=6)
    limbs = [ax_run.plot([], [], 'k-', lw=2)[0] for _ in range(4)]  # 2 legs, 2 arms

    # Data lines
    line_vx, = ax_data.plot([], [], label='Speed (vx)')
    line_ke, = ax_data.plot([], [], label='KE')
    line_pe, = ax_data.plot([], [], label='PE')
    ax_data.set_xlim(0, params['total_time'])
    ax_data.set_ylim(0, np.max(ke)*1.1)
    ax_data.legend(loc='upper right')

    text_metrics = ax_run.text(0.05, 1.8, '', fontsize=10)

    t_vals = np.linspace(0, params['total_time'], len(x))
    def init():
        bg_line.set_data([], [])
        torso.set_data([], [])
        head.set_data([], [])
        for limb in limbs:
            limb.set_data([], [])
        line_vx.set_data([], [])
        line_ke.set_data([], [])
        line_pe.set_data([], [])
        return [bg_line, torso, head, *limbs, line_vx, line_ke, line_pe, text_metrics]

    def update(i):
        t = i * params['time_step']
        hip = np.array([0.0, y[i]])
        shoulder = hip + np.array([0, params['torso_len']])
        head_pos = shoulder + np.array([0, 0.1])

        # Joint angles
        hip_a, knee_a, sh_a, el_a = gait_angles(t, params['stride_frequency'])

        # Legs
        knee = hip + params['thigh_len'] * np.array([np.sin(hip_a), -np.cos(hip_a)])
        foot = knee + params['shank_len'] * np.array([np.sin(hip_a + knee_a), -np.cos(hip_a + knee_a)])

        # Arms
        elbow = shoulder + params['upper_arm_len'] * np.array([np.sin(sh_a), -np.cos(sh_a)])
        hand = elbow + params['forearm_len'] * np.array([np.sin(sh_a + el_a), -np.cos(sh_a + el_a)])

        # Set body
        torso.set_data([hip[0], shoulder[0]], [hip[1], shoulder[1]])
        head.set_data(head_pos[0], head_pos[1])
        limbs[0].set_data([hip[0], knee[0]], [hip[1], knee[1]])
        limbs[1].set_data([knee[0], foot[0]], [knee[1], foot[1]])
        limbs[2].set_data([shoulder[0], elbow[0]], [shoulder[1], elbow[1]])
        limbs[3].set_data([elbow[0], hand[0]], [elbow[1], hand[1]])

        # Background scroll
        offset = -x[i]
        bg_line.set_data(bg_x + offset, bg_y)

        # Data
        line_vx.set_data(t_vals[:i], vx[:i])
        line_ke.set_data(t_vals[:i], ke[:i])
        line_pe.set_data(t_vals[:i], pe[:i])

        text_metrics.set_text(f"Speed: {vx[i]:.2f} m/s\nKE: {ke[i]:.1f} J\nPE: {pe[i]:.1f} J")

        return [bg_line, torso, head, *limbs, line_vx, line_ke, line_pe, text_metrics]

    ani = animation.FuncAnimation(
        fig, update, frames=len(x), init_func=init, blit=True, interval=20)
    plt.tight_layout()
    plt.show()
