import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

max_particles=40

#radius and positions
radius=0.2
position=np.random.rand(max_particles,2)*20
#print(position)

#Velocities
speed=0.2
velocities=np.random.randn(max_particles,2)
#print(velocities)

#occupancies
occupancies=[2]*int(max_particles/2) + [0]*int(max_particles/2)
#print(occupancies)

#Generating the canvas of the plot; Two plots are generated
fig,ax=plt.subplots()
fig1,ax1=plt.subplots()

#First plot shows the movement of the molecule
#Title of the plot
fig.text(0.4, 0.95, "Nanoreactor", color="black", fontsize=16)
fig.text(0.13, 0.9, "Red ball:O radical", backgroundcolor="red", color="white")
fig.text(0.36, 0.9, "Green ball:O2 molecule", backgroundcolor="green", color="white")
fig.text(0.65, 0.9, "Blue Ball:O3 molecule", backgroundcolor="blue", color="white")
ax.set_xlim(0,20)
ax.set_xticks([])
ax.set_ylim(0,20)
ax.set_yticks([])
ax.set_xlabel("Box Size: 20x20 units", color='white',backgroundcolor="black", fontsize=14)


#Second plot shows the variation of the composition with time graphically
#Title of the plot
ax1.set_title("Variation of Composition with time in nanoreactor", color="black", fontsize=14)
ax1.set_xticks([])
ax1.set_xlabel("Time", fontsize=14)
ax1.set_ylabel("Number of the species",fontsize=14)
ax1.set_xlim(0,20)
ax1.set_ylim(0,30)


#Initialization of plot for representing the composition
#line1 (red) represents the number of O radicals
y1=[0]*20
line1, =ax1.plot(y1,'o', label='O radical')
line1.set_color('red')

#line2 (green) represents the number of O2 molecules
y2=[0]*20
line2, =ax1.plot(y2, label='O2 molecule')
line2.set_color('green')

#line3 (blue) represents the number of O3 molecules
y3=[0]*20
line3, =ax1.plot(y3, '--b', label='O3 molecule')
#line3.set_color('blue')

#legends position
leg=ax1.legend(loc="upper right")

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
		print(occupancies.count(0))
	#####   When O3 is activated by hnu
	elif occupancies[i]==3 and j==-1:
		new_particle=checkZero()
		occupancies[i]=2
		occupancies[new_particle]=1
		color_update(i)
		color_update(new_particle)
		print(occupancies.count(0))
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
		print(occupancies.count(0))
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
		print(occupancies.count(0))
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
		print(occupancies.count(0))
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
		print(occupancies.count(0))
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
		print(occupancies.count(0))

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
			if position[i][0]<= radius or position[i][0] >= 20-radius:
				velocities[i][0]*=-1
				#Ensure the particle is inside the boundary
				position[i][0]=max(min(position[i][0],20-radius),radius)
			if position[i][1]<= radius or position[i][1] >= 20-radius:
				velocities[i][1]*=-1
				#Ensure the particle is inside the boundary
				position[i][1]=max(min(position[i][1],20-radius),radius)
			#Check for collisions
			check_collisions()
		particles[i].set_center(position[i])
	#Activation by radiation
	hnu=np.random.randint(0,1000)
	if hnu<5:
		act_mol=np.random.randint(0,max_particles)
		check_reactions(act_mol,-1)


	return particles

def update1(graph):
	#updating the data for plot

	#updating the number of radicals
	y1.pop(0)
	y1.append(occupancies.count(1))
	line1.set_ydata(y1)

	#updating the number of oxygens(O2)
	y2.pop(0)
	y2.append(occupancies.count(2))
	line2.set_ydata(y2)

	#updating the number of ozone(O3)
	y3.pop(0)
	y3.append(occupancies.count(3))
	line3.set_ydata(y3)

	return line1,line2,line3

for i in range(max_particles):
	ax.add_patch(particles[i])
	color_update(i)


ani=animation.FuncAnimation(fig, update, frames=500, interval=50, blit=True)
ani1=animation.FuncAnimation(fig1, update1, frames=500, interval=50, blit=True)
plt.show()
