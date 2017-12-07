import numpy as np
import matplotlib.pyplot as plt
import random

plt.close() # make sure we have a new plot (unnecessary in this example)
plt.xlim([-2, 255+2]) # change the range to add a little spacing

# we make a dictionary, one per class
# this is an excessively complicated way to approach this, probably!
myvalues = {}
for n in range(4):
	myvalues[n] = []

# then we fill in our data - for the example this is just random!
for n in range(256):
	myclass = n % 4 # not really, of course
	myvalue = random.randint(5, 20) # the same!
	# x value, y value, low error, high error - we unzip this below
	data = (n, myvalue, 1.5, 0.5, "type " + str(n))
	# append our data to the relevant class
	myvalues[myclass].append(data)

for n in range(4):
	# transform our lists of 4 values, to 4 lists of values
	# (you can also just append to four different lists!)
	(x, y, low, high, names) = zip(*myvalues[n])
	# x values, y values, error values
	plt.errorbar(x, y, yerr=[low, high], fmt = 'o', label = "class " + str(n), color = np.random.rand(3, 1))

	# also add names to the x axis (notice how they don't all show up, due to space) 
	plt.xticks(x, names, size='small', rotation=90)

	# you could also try other representations; for example, scatter:
	# some_markers = ['+', '>', (5, 0), (5, 1)]
	# plt.scatter(x, y, c = np.random.rand(3, 1), marker = some_markers[n], s = 50, label = "class " + str(n))

# add a legend (using the labels from before) and show the figure
plt.legend()
plt.show()
