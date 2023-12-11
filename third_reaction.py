import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

max_particles=40

#radius and positions
radius=0.2
position=np.random.rand(max_particles,2)*20
print(position)

#Velocities
speed=0.2
velocities=np.random.rand(max_particles,2)
print(velocities)

#occupancies
occupancies=np.zeros(max_particles)
occupancies[:int(max_particles/2)]=2
#occupancies[int(max_particles/2)+1]=1
#occupancies[int(max_particles/2)+2]=3
print(occupancies)

fig,ax=plt.subplots()
ax.set_xlim(0,20)
ax.set_ylim(0,20)

#Draw the Circle
particles=[plt.Circle(position[i], radius) for i in range(max_particles)]

#Set the Color
def color_update(i):
	if occupancies[i]==0:   # dummy particle bears white color
		particles[i].set_color('white')
	elif occupancies[i]==1: # particle with single atom (O) bears red color
		particles[i].set_color('red')
	elif occupancies[i]==2: # particle with two atoms (O2) bears green color
		particles[i].set_color('green')
	else:                   #particle with three atoms (O3) bears blue color
		particles[i].set_color('blue')


#Check Zero Occupancy; Required for filling a newly generated atom or molecule
def checkZero():
	for i in range(max_particles):
		if occupancies[i]==0:
			return i

#Function to check the colliding particles occupancies and make reaction
def check_reactions(i,j):
	#####   When O2 is activated by hnu
	if occupancies[i]==2 and j==-1:
		new_particle=checkZero()
		occupancies[i]=1
		occupancies[new_particle]=1
		color_update(i)
		color_update(new_particle)
		print(occupancies)
	#####   When O3 is activated by hnu
	elif occupancies[i]==3 and j==-1:
		new_particle=checkZero()
		occupancies[i]=2
		occupancies[new_particle]=1
		color_update(i)
		color_update(new_particle)
		print(occupancies)
	#####   When O2 collides with another O2 (No reaction)
	elif occupancies[i]==2 and occupancies[j]==2:
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
	#####   When O3 collides with another O3 (No reaction)
	elif occupancies[i]==3 and occupancies[j]==3:
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
	#####   When O2 collides with another O3 (No reaction)
	elif occupancies[i]==2 and occupancies[j]==3:
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
	####   When O radical collides with O radical
	elif (occupancies[i]==1 and occupancies[j]==1):
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		occupancies[i]=2
		occupancies[j]=0
		color_update(i)
		color_update(j)
		print(occupancies)
	#####   When O3 collides with another O2 (No reaction)
	elif occupancies[i]==3 and occupancies[j]==2:
		direction_i = position[i]-position[j]
		direction_j = position[j]-position[i]
		velocities[i]=direction_i/np.linalg.norm(direction_i)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
		velocities[j]=direction_j/np.linalg.norm(direction_j)*speed
	####   When O radical collides with O2 molecule
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
	####   When O2 molecule collides with O radical
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
	####    When O3 molecule collides with O radical
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
	####    When O radical collides with O3 molecule
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
				#Ensure the particle is inside the boundary
				position[i][0]=max(min(position[i][0],20),0)
			if position[i][1]<= 0 or position[i][1] >= 20:
				velocities[i][1]*=-1
				#Ensure the particle is inside the boundary
				position[i][1]=max(min(position[i][1],20),0)
			#Check for collisions
			check_collisions()
		particles[i].set_center(position[i])
	#Activation by radiation
	hnu=np.random.randint(0,1000)
	if hnu<5:
		act_mol=np.random.randint(0,max_particles)
		check_reactions(act_mol,-1)
	return particles




for i in range(max_particles):
	ax.add_patch(particles[i])
	color_update(i)

ani=animation.FuncAnimation(fig, update, frames=500, interval=50, blit=True)
plt.show()
