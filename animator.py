# Rendering loop

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate(x, y, vx, vy, ke, pe, params):
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1])
    ax_anim = fig.add_subplot(gs[0, :])
    ax_plot = fig.add_subplot(gs[1, :])

    line_speed, = ax_plot.plot([], [], label='Speed (vx)', color='blue')
    line_ke, = ax_plot.plot([], [], label='KE', color='orange')
    line_pe, = ax_plot.plot([], [], label='PE', color='green')
    ax_plot.set_xlim(0, params["total_time"])
    ax_plot.set_ylim(0, max(ke.max(), pe.max()) * 1.1)
    ax_plot.set_xlabel("Time (s)")
    ax_plot.legend()

    body, = ax_anim.plot([], [], 'ko-', lw=2)
    bg_scroll = np.linspace(0, 50, 500)
    skyline = 1.8 + 0.05*np.sin(bg_scroll / 1.5)
    sidewalk = np.zeros_like(bg_scroll)
    ax_anim.plot(bg_scroll, skyline, color='skyblue', linewidth=2)
    ax_anim.plot(bg_scroll, sidewalk, color='black', linewidth=2)

    ax_anim.set_xlim(-1, 1)
    ax_anim.set_ylim(0, 2)

    text = ax_anim.text(-0.9, 1.9, '', fontsize=9, bbox=dict(facecolor='white', alpha=0.7))

    def update(frame):
        t = frame * params["dt"]
        cx = 0.0
        cy = y[frame]
        limb = params["limb_length"]

        torso_top = (cx, cy + params["torso_length"])
        torso_bottom = (cx, cy)
        head = (cx, cy + params["torso_length"] + params["head_radius"])

        leg_theta = params["leg_swing_amp"] * np.sin(2 * np.pi * params["leg_angular_freq"] * t)
        leg1 = (cx + limb * np.sin(leg_theta), cy - limb * np.cos(leg_theta))
        leg2 = (cx - limb * np.sin(leg_theta), cy - limb * np.cos(leg_theta))

        arm_theta = params["arm_swing_amp"] * np.sin(2 * np.pi * params["leg_angular_freq"] * t + np.pi)
        arm1 = (cx + limb * np.sin(arm_theta), cy + 0.6 * limb * np.cos(arm_theta))
        arm2 = (cx - limb * np.sin(arm_theta), cy + 0.6 * limb * np.cos(arm_theta))

        stick_x = [leg1[0], torso_bottom[0], leg2[0], torso_bottom[0], torso_top[0], arm1[0], torso_top[0], arm2[0], torso_top[0], head[0]]
        stick_y = [leg1[1], torso_bottom[1], leg2[1], torso_bottom[1], torso_top[1], arm1[1], torso_top[1], arm2[1], torso_top[1], head[1]]
        body.set_data(stick_x, stick_y)

        history = slice(0, frame+1)
        time_axis = np.linspace(0, t, frame+1)
        line_speed.set_data(time_axis, vx[history])
        line_ke.set_data(time_axis, ke[history])
        line_pe.set_data(time_axis, pe[history])

        text.set_text(f"t = {t:.2f}s\nSpeed = {vx[frame]:.2f} m/s\nHeight = {y[frame]:.2f} m")
        return body, line_speed, line_ke, line_pe, text

    ani = animation.FuncAnimation(fig, update, frames=len(x), interval=30, blit=True)
    plt.tight_layout()
    plt.show()

