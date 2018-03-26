from random import randint
from .file_access import get_data

class message:
	msgs = []
	
	def __init__(self, filename='', data=[]):
		if filename != '':
			self.msgs = self.msgs + get_data(filename, 's')
		elif len(data) > 0:
			self.msgs = self.msgs + data
	
	def rnd_msg(self):
		return self.msgs[randint(0, len(self.msgs)-1)]
	
	def find(self, ref):
		for i in range(len(self.msgs)):
			if self.msgs[i] == ref:
				return i
		return -1
	
	def __str__(self):
		s = ''
		for i in range(len(self.msgs)):
			if i > 0:
				s += ', '
			s += self.msgs[i]
		return s