import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Ball:
    def __init__(self, x, y, vx, vy, radius=0.5, styles=None):
        """Initialize the particle's position, velocity, radius and color."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.styles = styles

    def update(self, dt):
        """Update the particle's position."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check for collisions with the box walls
        if self.x < self.radius:
            self.vx = -self.vx
            self.x = self.radius
        elif self.x > box_width - self.radius:
            self.vx = -self.vx
            self.x = box_width - self.radius

        if self.y < self.radius:
            self.vy = -self.vy
            self.y = self.radius
        elif self.y > box_height - self.radius:
            self.vy = -self.vy
            self.y = box_height - self.radius

    def collide(self, other):
        """Handle a collision with another ball."""

        # Calculate the distance between the centers of the balls
        distance = np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

        # If the distance is less than the sum of their radii, then the balls are colliding
        if distance < self.radius + other.radius:

            # Calculate the relative velocity between the balls
            relative_velocity = np.array([self.vx - other.vx, self.vy - other.vy])

            # Calculate the normal vector to the line connecting the centers of the balls
            normal_vector = np.array([self.x - other.x, self.y - other.y]) / distance

            # Reflect the relative velocity across the normal vector
            reflected_velocity = relative_velocity - 2 * (relative_velocity.dot(normal_vector)) * normal_vector

            # Update the velocities of the balls
            self.vx = self.vx - reflected_velocity[0]
            self.vy = self.vy - reflected_velocity[1]
            other.vx = other.vx + reflected_velocity[0]
            other.vy = other.vy + reflected_velocity[1]

    def plot(self, ax):
        """Plot the ball on the matplotlib axis."""
        circle = plt.Circle((self.x, self.y), radius=self.radius, color=self.styles)
        ax.add_patch(circle)

# Define the box dimensions
box_width = 10
box_height = 10

# Create a list of 10 balls
balls = []
for i in range(10):
    x = np.random.rand() * box_width
    y = np.random.rand() * box_height
    vx = np.random.randn()
    vy = np.random.randn()

    # Create a new ball with the random values
    ball = Ball(x, y, vx, vy)

    # Add the ball to the list of balls
    balls.append(ball)

# Define the animation function
def animate(frame_number):
    """Update the positions of all the balls and plot them."""

    # Update the positions of all the balls
    for ball in balls:
        ball.update(0.01)

    # Check for collisions between the balls
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].collide(balls[j])

    # Clear the plot
    ax.clear()

    # Plot all the balls
    for ball in balls:
        ball.plot(ax)

    # Set the axis limits
    ax.set_xlim(0, box_width)
    ax.set_ylim(0, box_height)

    # Update the title
    ax.set_title('Bouncing Balls Animation')

# Create a new figure
fig, ax = plt.subplots()

# Create an animation
ani=FuncAnimation(fig, animate, interval=10, blit=True)

plt.show()
