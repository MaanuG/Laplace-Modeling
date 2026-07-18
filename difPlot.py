import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


frames = []
times = []

with open("diffusion.txt", "r") as f:

    current = []

    for line in f:

        line = line.strip()

        if line == "":
            continue

        if line.startswith("====="):

            if current:
                frames.append(np.array(current))
                current = []

            time = float(line.replace("=", "").replace("Time", "").strip())
            times.append(time)

        else:

            tokens = line.split()

            x = float(tokens[1])
            y = float(tokens[3])
            rho = float(tokens[5])

            current.append([x, y, rho])

if current:
    frames.append(np.array(current))


x = np.unique(frames[0][:,0])
y = np.unique(frames[0][:,1])

X, Y = np.meshgrid(x, y, indexing="ij")

nx = len(x)
ny = len(y)


fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection="3d")

zmax = max(frame[:,2].max() for frame in frames)

def update(frame_number):

    ax.clear()

    data = frames[frame_number]

    Z = data[:,2].reshape(nx, ny)

    ax.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        edgecolor="k",
        linewidth=0.2
    )

    ax.set_title(f"2D Diffusion\nTime = {times[frame_number]:.3f} s")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel(r"$\rho$")

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(0, zmax)

ani = FuncAnimation(
    fig,
    update,
    frames=len(frames),
    interval=200
)

plt.show()
