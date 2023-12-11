import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

max_particles=20

#positions
radius=0.5
position=np.random.rand(max_particles,2)*20
print(position)

#Velocities
speed=1.0
velocities=np.random.rand(max_particles,2)
print(velocities)

#occupancies
occupancies=np.zeros(max_particles)
occupancies[:int(max_particles/2)]=2
occupancies[int(max_particles/2)+1]=1
occupancies[int(max_particles/2)+2]=3
print(occupancies)

fig=plt.figure(facecolor='black')
ax=fig.add_subplot()
ax.set_facecolor('black')
ax.spines['bottom'].set_color('brown')
ax.spines['top'].set_color('brown')
ax.spines['left'].set_color('brown')
ax.spines['right'].set_color('brown')
ax.tick_params(axis='x', color='brown')
ax.tick_params(axis='y', color='brown')
ax.set_xlim(0,20)
ax.set_ylim(0,20)

#Set the Color
def color_update(i):
	if occupancies[i]==0:
		particles[i].set_color('black')
	elif occupancies[i]==1:
		particles[i].set_color('red')
	elif occupancies[i]==2:
		particles[i].set_color('green')
	else:
		particles[i].set_color('blue')



#Function to check the colliding particles occupancies and make reaction
def check_reactions(i,j):
	if occupancies[i]==2 and occupancies[j]==2:
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
	elif (occupancies[i]==1 and occupancies[j]==2):
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		occupancies[i]=0
		occupancies[j]=3
		color_update(i)
		color_update(j)
		print(occupancies)
	elif (occupancies[i]==2 and occupancies[j]==1):
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		occupancies[i]=3
		occupancies[j]=0
		color_update(i)
		color_update(j)
		print(occupancies)
	elif (occupancies[i]==3 and occupancies[j]==1):
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		occupancies[i]=2
		occupancies[j]=2
		color_update(i)
		color_update(j)
		print(occupancies)
	elif (occupancies[i]==1 and occupancies[j]==3):
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		occupancies[i]=2
		occupancies[j]=2
		color_update(i)
		color_update(j)
		print(occupancies)

#Function to check for particle-particle collisions
def check_collisions():
	for i in range(max_particles):
		if occupancies[i]>0:
			for j in range(i+1, max_particles):
				if occupancies[j]>0:
					distance=np.linalg.norm(position[i]-position[j])
					if distance < 2*radius:
						#Collision detected
						check_reactions(i,j)


def update(frame):
	for i in range(max_particles):
		if occupancies[i]>0:
			position[i] +=velocities[i]

			#Bounce off the walls
			if position[i][0]<= 0 or position[i][0] >= 20:
				velocities[i][0]*=-1
			if position[i][1]<= 0 or position[i][1] >= 20:
				velocities[i][1]*=-1
			#Check for collisions
			check_collisions()
		particles[i].set_center(position[i])
	return particles


#Draw the Circle
particles=[plt.Circle(position[i], radius) for i in range(max_particles)]



for i in range(max_particles):
	ax.add_patch(particles[i])
	color_update(i)

ani=animation.FuncAnimation(fig, update, frames=500, interval=50, blit=True)
plt.show()
