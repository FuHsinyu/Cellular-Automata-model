import numpy as np
import random
from random import randint as randi
import math

from pyics import Model

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

EMPTINESS = 0
white = [1, 1, 1, 1]

def clamp(val, _min, _max):
	if _min > _max:
		[_min, _max] = [_max, _min]
	return max(_min, min(val, _max))
	
def inverse_power(alpha, p):
	result = p ** (-1 / alpha)
#	print(result)
	return result

def norm_pdf(x, mean, stdev):
	result = ((2 * math.pi * stdev ** 2) ** (-.5)) * (math.e ** (-((x - mean) ** 2) / (2 * stdev ** 2)))
	return clamp(result, 0, 1) 
	
def inverse_norm(mean, stdev, p):
	sign = 1 if random.random() > .5 else -1 # positive or negative relative to the mean
	tmp = -math.log(2 * math.pi * (p ** 2) * (stdev ** 2))
	if tmp < 0:
		tmp = 0
	return mean + sign * stdev * tmp ** .5

def plot_distr(alpha, name):
	x = []
	y = []
	p = 0.001
	while p <= 1:
		x.append(p)
		y.append(inverse_power(alpha, p))
		p += 0.001
	plt.plot(x, y)
	plt.title(name)
	plt.grid()
	
def matrix(value, width, height):
	return [[value for i in range(width)] for j in range(height)]

class CA1D(Model):
	def __init__(self):
		Model.__init__(self)
		
		self.make_param('width', 30, setter = self.set_positive_int)
		self.make_param('height', 30, setter = self.set_positive_int)
		self.make_param('r', 1, setter = self.set_positive_int)
		self.make_param('parties', 2, setter = self.set_positive_int)
		self.make_param('humans_density', 0.65, setter = self.set_fraction)
		
		self.make_param('humans_density', 0.65, setter = self.set_fraction)
		
		self.make_param('alpha_influence', 2.)
		
		self.make_param('mean_conviction', 5.)
		self.make_param('stdev_conviction', 1e-6, setter = self.set_stdev)
		
		self.parties_count = 0
		self.humans_count = 0
		self.parties_data = []		
		
		self.colorbar = None
		
	def set_positive_int(self, val):
		return max(1, int(val))
	
	def set_fraction(self, val):
		return clamp(val, 0, 1)
	
	def set_stdev(self, val):
		return val if val > 1e-6 else 1e-6
		
	def init_field(self):
		field = matrix(EMPTINESS, self.width, self.height)
		self.image = matrix(EMPTINESS, self.width, self.height)
		
		free_space = [[i, j] for i in range(self.width) for j in range(self.height)]

		tmp_counter = self.humans_count
		
		self.humans = []
		
		for party in range(self.parties):
			count = int(clamp(math.ceil(self.parties_data[party]['fraction'] * self.humans_count), 0, tmp_counter))
			self.party_counts.append(count)
			
			tmp_counter -= count

			for humans in range(count):
				[x, y] = free_space.pop(randi(0, len(free_space) - 1))
				
				human = {'party' : party + 1,
						'influence' : inverse_power(self.alpha_influence, random.random()),
					#	'conviction': inverse_power(self.alpha_conviction, random.random()),
						'conviction': inverse_norm(self.mean_conviction, self.stdev_conviction, random.random()),
						'position': [x, y]}
				
				self.humans.append(human)
				field[y][x] = human
				self.image[y][x] = 	party + 1
				
			for human in self.humans:
				[x, y] = human['position']
				minx = max(x - self.r, 0)
				maxx = min(x + self.r + 1, len(field[0]))
				miny = max(y - self.r, 0)
				maxy = min(y + self.r + 1, len(field))
				human['neighbourhood'] = []
				
				for j in range(miny, maxy):
					for i in range(minx, maxx):
						neighbour = field[j][i]
						if neighbour and not (x == i and y == j):
							human['neighbourhood'].append(neighbour)
			
	def reset(self):
		#	still a bit buggy
		self.t = 1

		cells = self.width * self.height
		self.humans_count = int(self.humans_density * cells)
		self.labels = ['Nothing']
		remainder = 1
		
		self.party_counts = []		
		new_parties = range(self.parties_count, self.parties)
		
		for party in new_parties:
			fraction = 1 / self.parties
			
			new_party = {
				'fraction' : fraction,
				'count': fraction * self.humans_count,
				'bias': 0}
			
			self.make_param('party%d_percentage' %(party + 1), float(new_party['fraction']))
			self.make_param('party%d_bias' %(party + 1), float(new_party['bias']))
			
			self.parties_data.append(new_party)
			remainder -= fraction
		
		old_parties = [party for party in range(self.parties_count)]
		
		if remainder == 1:	# nothing's been added
			for party in old_parties:
				param_name = 'party%d_' %(party + 1)
				
				fraction = getattr(self, param_name + 'percentage')
				
				if self.parties_data[party]['fraction'] != fraction: # this one's been modidfied
					remainder = (1 - fraction) / (1 - self.parties_data[party]['fraction'])
					self.parties_data[party]['fraction'] = fraction / remainder
					self.parties_data[party]['count'] = fraction * self.humans_count / remainder
					break
		
		for party in old_parties:
			param_name = 'party%d_' %(party + 1)
			
			self.parties_data[party]['fraction'] *= remainder
			self.parties_data[party]['count'] *= remainder
			self.parties_data[party]['bias'] = getattr(self, param_name + 'bias')
			
			exec ('self.' + param_name + 'percentage = %f' %self.parties_data[party]['fraction'])
						
		for i in range(self.parties):
			self.labels.append('Party #%d' %(i + 1))
		
		self.parties_count = self.parties
		self.init_field()
		
		self.data = [[party['fraction']] for party in self.parties_data]
		
		if self.gui:
			self.gui.reset_params()
		
		self.cmap = np.vstack((white, plt.cm.Set1([i for i in range(self.parties)])))
		self.cmap = mpl.colors.ListedColormap(self.cmap)
		
		if self.colorbar:
			self.colorbar.remove()
			self.colorbar = None
			
		
	def step(self):
		something_new = False
		
		for human in self.humans:
			
			max_influence = self.parties_data[0]['bias']
			preferable_party = 1

			influence = {preferable_party: max_influence}
			for i in range(1, len(self.parties_data)):
				influence[i + 1] = self.parties_data[i]['bias']
				if influence[i + 1] > max_influence:
					max_influence = influence[i + 1]
					preferable_party = i + 1
			
			influence[human['party']] += human['conviction']
			if influence[human['party']] > max_influence:
				preferable_party = human['party']
				max_influence = influence[preferable_party]
			
			self.party_counts[human['party'] - 1] -= 1
			
			for neighbour in human['neighbourhood']:
				
				party = neighbour['party']
				
				if party in influence:
					influence[party] += neighbour['influence']
				else:
					influence[party] = neighbour['influence']
				
				if influence[party] > max_influence:
					max_influence = influence[party]
					preferable_party = party
				
				elif influence[party] == max_influence:
					max_influence = human['conviction']
					preferable_party = human['party']
				
			if preferable_party != human['party']:
				something_new = True
				
			[x, y] = human['position']
			self.image[y][x] = preferable_party
		
		for human in self.humans:
			[x, y] = human['position']
			human['party'] = self.image[y][x]
			self.party_counts[human['party'] - 1] += 1
		
		for i in range(len(self.party_counts)):
			count = self.party_counts[i]
			self.data[i].append(count / self.humans_count)
		
		self.t += 1
		
		if not something_new and self.gui:
			self.gui.stopRunning()
		
		
	def draw(self):
		for party in range(self.parties):
			print(self.data[party][self.t - 1])
		print()
		
		if self.colorbar is None:
			bounds = [i for i in range(self.parties + 2)]

			norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N + 1)
			plt.clf()
			if not plt.gca().yaxis_inverted():
				plt.gca().invert_yaxis()
			
			plt.subplot(121)
			self.image_data = plt.imshow(self.image, interpolation = 'none', cmap = self.cmap, norm = norm)
			
			self.colorbar = plt.colorbar(orientation='horizontal')
			self.colorbar.set_ticks(list(map(lambda x: x + 0.5, bounds[:-1])))
			self.colorbar.ax.set_xticklabels(self.labels)
			
			plot = plt.subplot(122)
			plt.xlabel('timesteps')
			plt.ylabel('Voter fraction')
			plot.yaxis.set_label_position("right")
			plot.yaxis.tick_right()
			plt.grid()
			plt.ylim([0, 1])
		else:
			self.image_data.set_data(self.image)
		
		plt.title('t = %d' % self.t)
		for party in range(self.parties):
			plt.plot(self.data[party], color = self.cmap(party + 1))
		plt.xlim([0, self.t])
