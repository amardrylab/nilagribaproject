import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Class to represent a ball
class Ball:
    def __init__(self, id, box_width, box_height):
        self.id = id
        self.x = np.random.rand() * box_width
        self.y = np.random.rand() * box_height
        self.vx = np.random.randn() * 0.2
        self.vy = np.random.randn() * 0.2

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Check for collisions with the box walls
        if self.x < 0:
            self.vx = -self.vx
            self.x = 0
        elif self.x > box_width:
            self.vx = -self.vx
            self.x = box_width

        if self.y < 0:
            self.vy = -self.vy
            self.y = 0
        elif self.y > box_height:
            self.vy = -self.vy
            self.y = box_height

    def plot(self):
        circle = plt.Circle((self.x, self.y), radius=0.2, color='red')
        plt.gca().add_patch(circle)

# Define the box dimensions
box_width = 10
box_height = 10
# Set the axis limits
# Update the title

# Create a list of 10 balls
balls = []
for i in range(10):
    ball = Ball(i, box_width, box_height)
    balls.append(ball)

# Define the animation function
def animate(frame_number):
    # Update the positions of all the balls
    for ball in balls:
        ball.update()

    # Clear the plot
    plt.clf()

    plt.xlim(0, box_width)
    plt.ylim(0, box_height)
    plt.title('Bouncing Balls Animation')

    # Plot the balls
    for ball in balls:
        ball.plot()



# Create a new figure
fig = plt.figure()

# Create an animation
animation = FuncAnimation(fig, animate, interval=10)

# Start the animation
plt.show()


