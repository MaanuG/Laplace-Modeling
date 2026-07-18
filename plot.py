import re
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# 1. Parse the laplace.txt file
data = {}
current_iteration = None

with open("laplace.txt", "r") as f:
    for line in f:
        # Detect iteration header
        iter_match = re.search(r"--- Iteration (\d+) ---", line)
        if iter_match:
            current_iteration = int(iter_match.group(1))
            data[current_iteration] = []
            continue

        # Parse coordinate lines
        if "x:" in line and "y:" in line:
            parts = line.split()
            x = float(parts[1])
            y = float(parts[3])
            v = float(parts[5])
            data[current_iteration].append((x, y, v))

# Get sorted list of available iterations
iterations = sorted(data.keys())

# Get global unique coordinates from the first step to build dimensions
sample_points = np.array(data[iterations[0]])
x_coords = np.unique(sample_points[:, 0])
y_coords = np.unique(sample_points[:, 1])


# Helper function to convert parsed point lists into a 2D grid matrix
def points_to_grid(points_list):
    grid = np.zeros((len(y_coords), len(x_coords)))
    for x, y, v in points_list:
        xi = np.where(x_coords == x)[0][0]
        yi = np.where(y_coords == y)[0][0]
        grid[yi, xi] = v
    return grid


# 2. Set up the plotting window
fig, ax = plt.subplots(figsize=(10, 6))

# Initialize the plot with the first iteration's grid layout
initial_grid = points_to_grid(data[iterations[0]])
heatmap = ax.imshow(
    initial_grid,
    extent=[x_coords.min(), x_coords.max(), y_coords.min(), y_coords.max()],
    origin="lower",
    cmap="RdYlBu_r",
    aspect="equal",
    vmin=0,
    vmax=8.0,  # Fixed boundaries prevent color scaling from shifting over time
)

# Static labels and aesthetic additions
ax.set_xlabel("X Position", fontsize=12)
ax.set_ylabel("Y Position", fontsize=12)
title_text = ax.set_title("", fontsize=14)
cbar = fig.colorbar(heatmap)
cbar.set_label("Voltage / Potential (V)", fontsize=12)


# 3. Animation Engine
def update(frame_idx):
    """Updates the frame data for each recorded milestone step."""
    current_iter = iterations[frame_idx]
    current_grid = points_to_grid(data[current_iter])

    # Push new grid array values into the existing visualization object
    heatmap.set_array(current_grid)
    title_text.set_text(f"2D Laplace Potential Grid - Iteration {current_iter}")
    return heatmap, title_text


# Create live playback wrapper
# interval=800 means each frame sits on screen for 800 milliseconds
ani = animation.FuncAnimation(
    fig, update, frames=len(iterations), interval=800, blit=True, repeat=True
)

plt.tight_layout()
plt.show()
