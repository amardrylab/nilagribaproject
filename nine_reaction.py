import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

max_particles=40
tsCounter=0
counter500=[0, 20, 0, 20, 0] ##[timeStep, vacantposition, O-radical, Oxygen, Ozone]

#seeding random number for reproducibility
#np.random.seed(400)

#radius 
radius=0.5

#position of the particles
position=np.random.rand(max_particles,2)*20
print(position)

#Velocities chosen from Gaussian distribution
speed=0.3
velocities=np.random.normal(loc=0.0, scale=1.0, size=(max_particles,2))*speed
print(velocities)

#occupancies
occupancies=[2]*int(max_particles/2) + [0]*int(max_particles/2)
print(occupancies)

#Generating the canvas of the plot; Three plots are generated
fig=plt.figure(figsize=(10,6))
gs=plt.GridSpec(3,8, hspace=0.4, wspace=1.1)
ax=plt.subplot(gs[0:,0:5])
ax1=plt.subplot(gs[0:2,5:])
ax2=plt.subplot(gs[-1,5:])
#fig1,ax1=plt.subplots()

#First plot shows the movement of the molecule
#Title of the plot
fig.text(0.2, 0.95, "Nanoreactor (Size: 20x20 units)", color="white",backgroundcolor="black", fontsize=13)
fig.text(0.13, 0.9, "Red ball:O radical", backgroundcolor="red", color="white", fontsize=9)
fig.text(0.265, 0.9, "Green ball:O2 molecule", backgroundcolor="green", color="white", fontsize=9)
fig.text(0.44, 0.9, "Blue Ball:O3 molecule", backgroundcolor="blue", color="white", fontsize=9)
ax.set_xlim(0,20)
ax.set_xticks([])
ax.set_ylim(0,20)
ax.set_yticks([])

#Initialization of plot for representing the molecules
#Draw the Circle
particles=[plt.Circle(position[i], radius) for i in range(max_particles)]

#Second plot shows the variation of the composition with time graphically
#Title of the plot
ax1.set_title("Variation of Composition with Time \nin Nanoreactor", color="black", fontsize=10)
ax1.set_xticks([])
ax1.set_xlabel("Time Steps", fontsize=8)
ax1.set_ylabel("Number of the species",fontsize=8)
ax1.set_xlim(0,20)
ax1.set_ylim(0,30)



#Initialization of plot for representing the composition
#line1 (red) represents the number of O radicals
y1=[0]*20
line1, =ax1.plot(y1,'o', label='O radical')
line1.set_color('red')

#line2 (green) represents the number of O2 molecules
y2=[20]*20
line2, =ax1.plot(y2, label='O2 molecule')
line2.set_color('green')

#line3 (blue) represents the number of O3 molecules
y3=[0]*20
line3, =ax1.plot(y3, '--b', label='O3 molecule')
line3.set_color('blue')

#legends position
leg=ax1.legend(loc="best")

#Time Step Counter
ts=ax1.annotate("Time Steps ={time}".format(time=tsCounter), xy=(4,20.7), fontsize=11)

#Append the elements of ax1 to particles (Required for update)
particles.append(line1)
particles.append(line2)
particles.append(line3)
particles.append(ts)


#Third plot shows the variation of the composition after each 500 time step
ax2.set_xticks([])
ax2.set_yticks([])


#Initialization of plot for representing composition after 500 time step
report0=ax2.annotate("After {timestep} Time Step(s)".format(timestep=0), xy=(0.1,0.8), fontsize=12)
report0.set_color('brown')
report1=ax2.annotate("Number of O radical(s) ={oxygen}".format(oxygen=0), xy=(0.1,0.6))
report1.set_color('red')
report2=ax2.annotate("Number of O2 molecule(s) ={oxygen}".format(oxygen=20), xy=(0.1,0.4))
report2.set_color('green')
report3=ax2.annotate("Number of O3 molecule(s) ={oxygen}".format(oxygen=0), xy=(0.1,0.2))
report3.set_color('blue')


#Append the elements of ax2
particles.append(report0)
particles.append(report1)
particles.append(report2)
particles.append(report3)



#Set the Color
def color_update(i):
	if occupancies[i]==0:   # dummy particle bears white color
		particles[i].set_color('white')
		particles[i].set_alpha(0)
	elif occupancies[i]==1: # particle with single atom (O) bears red color
		particles[i].set_color('red')
		particles[i].set_alpha(1)
	elif occupancies[i]==2: # particle with two atoms (O2) bears green color
		particles[i].set_color('green')
		particles[i].set_alpha(1)
	else:                   #particle with three atoms (O3) bears blue color
		particles[i].set_color('blue')
		particles[i].set_alpha(1)

for i in range(max_particles):
	ax.add_patch(particles[i])
	color_update(i)


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
		#Fixing a new position of the newly generated particle
		r=np.random.normal(loc=0.0, scale=2.0, size=2)
		position[new_particle]=position[i]+r
		occupancies[new_particle]=1
		color_update(new_particle)
		#Fixing a new position of i
		r=np.random.normal(loc=0.0, scale=2.0, size=2)
		position[i]+=r
		occupancies[i]=1
		color_update(i)
		print(occupancies)
	#####   When O3 is activated by hnu
	elif occupancies[i]==3 and j==-1:
		new_particle=checkZero()
		#Fixing a new position of the newly generated particle
		r=np.random.normal(loc=0.0, scale=2.0, size=2)
		position[new_particle]=position[i]+r
		occupancies[new_particle]=1
		color_update(new_particle)
		#Fixing a new position of i
		r=np.random.normal(loc=0.0, scale=2.0, size=2)
		position[i]+=r
		occupancies[i]=2
		color_update(i)
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
		#center of the two combining particles
		position[i][0]=(position[i][0]+position[j][0])/2
		position[i][1]=(position[i][1]+position[j][1])/2
		#Assigning velocities form Gaussian distribution
		velocities[i]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
		#velocities[j]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
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
		#center of the two combining particles
		position[j][0]=(position[i][0]+position[j][0])/2
		position[j][1]=(position[i][1]+position[j][1])/2
		#Assigning velocities form Gaussian distribution
		#velocities[i]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
		velocities[j]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
		occupancies[i]=0
		occupancies[j]=3
		color_update(i)
		color_update(j)
		print(occupancies)
	####   When O2 molecule collides with O radical
	elif (occupancies[i]==2 and occupancies[j]==1):
		#center of the two combining particles
		position[i][0]=(position[i][0]+position[j][0])/2
		position[i][1]=(position[i][1]+position[j][1])/2
		#Assigning velocities form Gaussian distribution
		velocities[i]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
		#velocities[j]=np.random.normal(loc=0.0, scale=1.0, size=2)*speed
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
	global tsCounter, counter500
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
	tsCounter+=1
	if (tsCounter%500) ==0:
		print(tsCounter)
		print(f'Number of vacant space {occupancies.count(0)}')
		print(f'Number of O radical {occupancies.count(1)}')
		print(f'Number of O2 molecule {occupancies.count(2)}')
		print(f'Number of O3 molecule {occupancies.count(3)}')
		spNo=[tsCounter, occupancies.count(0), occupancies.count(1), occupancies.count(2), occupancies.count(3)]
		counter500=spNo
		print(counter500)
	#Activation by radiation
	hnu=np.random.randint(0,1000)
	if hnu<=5:
		act_mol=np.random.randint(0, max_particles)
		while (occupancies[act_mol]==0 or occupancies[act_mol]==1):
			act_mol=np.random.randint(0,max_particles)
		check_reactions(act_mol,-1)


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

	#updating the tsCounter
	ts.set_text("Time Steps ={time}".format(time=tsCounter))
	particles[max_particles]=line1
	particles[max_particles+1]=line2
	particles[max_particles+2]=line3
	particles[max_particles+3]=ts

	#updating the reports
	report0.set_text("After {timestep} Time Step(s)".format(timestep=counter500[0]))
	report1.set_text("Number of O radical(s) ={oxygen}".format(oxygen=counter500[2]))
	report2.set_text("Number of O2 molecule(s) ={oxygen}".format(oxygen=counter500[3]))
	report3.set_text("Number of O3 molecule(s) ={oxygen}".format(oxygen=counter500[4]))

	particles[max_particles+4]=report0
	particles[max_particles+5]=report1
	particles[max_particles+6]=report2
	particles[max_particles+7]=report3

	return particles


ani=animation.FuncAnimation(fig, update, frames=500, interval=50, blit=True)
#ani1=animation.FuncAnimation(fig, update1, frames=500, interval=50, blit=True)
#ani2=animation.FuncAnimation(fig, update2, frames=100, interval=10, blit=True)
plt.show()
