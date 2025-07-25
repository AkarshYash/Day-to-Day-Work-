import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')
ax.axis('off')

# Create the line object
line, = ax.plot([], [], lw=2, color='cyan')

# Set up the limits of the plot
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Function to generate spiral + wave
def generate_art(t):
    theta = np.linspace(0, 10 * np.pi, 1000)
    r = np.linspace(0, 10, 1000)
    
    # Fusion of spiral and sine wave
    x = r * np.cos(theta + t) + 0.5 * np.sin(5 * theta + t)
    y = r * np.sin(theta + t) + 0.5 * np.cos(5 * theta - t)
    return x, y

# Init function
def init():
    line.set_data([], [])
    return line,

# Update function for animation
def update(frame):
    x, y = generate_art(frame / 10)
    line.set_data(x, y)
    return line,

# Animate
ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=30)

plt.show()
