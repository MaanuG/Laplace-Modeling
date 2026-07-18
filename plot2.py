import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = np.loadtxt("potential.dat")

print("Data shape:", data.shape)

# Extract coordinates
x = np.unique(data[:, 0])
y = np.unique(data[:, 1])

nx = len(x)
ny = len(y)

# Create coordinate grid
X, Y = np.meshgrid(x, y, indexing="ij")

# Reshape potential into matrix
V = data[:, 2].reshape(nx, ny)

print("Potential range:", V.min(), "to", V.max())

# Calculate electric field
Ex = np.zeros_like(V)
Ey = np.zeros_like(V)

dx = x[1] - x[0]
dy = y[1] - y[0]

Ex[1:-1, :] = -(V[2:, :] - V[:-2, :]) / (2 * dx)
Ey[:, 1:-1] = -(V[:, 2:] - V[:, :-2]) / (2 * dy)


plt.figure(figsize=(8, 6))

# Filled potential map
filled = plt.contourf(
    X,
    Y,
    V,
    levels=40,
    cmap="viridis"
)

# Equipotential lines
lines = plt.contour(
    X,
    Y,
    V,
    levels=20,
    colors="white",
    linewidths=1
)

plt.clabel(lines, fontsize=8)

plt.colorbar(
    filled,
    label="Potential (V)"
)

# Electric field lines
plt.streamplot(
    x,
    y,
    Ex.T,
    Ey.T,
    density=1.2,
    color="black",
    linewidth=0.8
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Potential and Equipotential Lines")

plt.gca().set_aspect("equal")

plt.show()