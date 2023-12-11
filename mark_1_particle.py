import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
num_particles = 20
box_size = 10
particle_radius = 0.2
speed = 0.1

# Initialize particle positions and velocities
positions = np.random.rand(num_particles, 2) * (box_size - 2 * particle_radius) + particle_radius
velocities = np.random.rand(num_particles, 2) * speed * 2 - speed

# Marked particle (choose a random particle to mark)
marked_particle = np.random.randint(0, num_particles)
marked_color = 'red'

# Create the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)

# Create a list of circles to represent the particles
particles = [plt.Circle(positions[i], particle_radius, color=marked_color if i == marked_particle else 'blue')
             for i in range(num_particles)]

# Add the circles to the plot
for particle in particles:
    ax.add_patch(particle)

# Variables to count collisions for the marked particle
marked_particle_collisions = 0

# Function to check for particle-particle collisions
def check_collisions():
#    nonlocal marked_particle_collisions
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            distance = np.linalg.norm(positions[i] - positions[j])
            if distance < 2 * particle_radius:
                # Collision detected, update velocities
                direction_i = positions[i] - positions[j]
                direction_j = positions[j] - positions[i]
                velocities[i] = direction_i / np.linalg.norm(direction_i) * speed
                velocities[j] = direction_j / np.linalg.norm(direction_j) * speed

                # Count collisions for the marked particle
                if i == marked_particle or j == marked_particle:
#                   marked_particle_collisions += 1

# Function to update particle positions
def update(frame):
    for i in range(num_particles):
        # Update positions
        positions[i] += velocities[i]

        # Bounce off the walls
        if positions[i][0] <= particle_radius or positions[i][0] >= box_size - particle_radius:
            velocities[i][0] *= -1
        if positions[i][1] <= particle_radius or positions[i][1] >= box_size - particle_radius:
            velocities[i][1] *= -1

        # Check for collisions
        check_collisions()

        # Update circle positions
        particles[i].set_center((positions[i][0], positions[i][1]))

    return particles

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=500, interval=50, blit=True)

# Display the animation
plt.show()

# Print the number of collisions for the marked particle
print(f"Number of collisions for marked particle: {marked_particle_collisions}")
