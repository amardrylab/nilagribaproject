import numpy as np
import matplotlib.pyplot as plt


myarray=np.zeros(100).reshape(20,5)
myarray[:,0]=np.random.randint(0,20,20)
myarray[:,1]=np.random.randint(0,20,20)
balls=myarray[:,0:2]
vel=(np.ones(40).reshape(20,2))

anim=plt.scatter(balls[:,0], balls[:,1])

for i in range(20):
	balls=balls+vel
	anim.set_offsets(balls)
	plt.draw()
	plt.pause(0.05)


print(myarray)

plt.show()
