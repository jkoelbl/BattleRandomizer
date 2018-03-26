def get_data(filename, style):
	args = {'': '[line for line in f]',
			's': '[line.strip() for line in f]',
			's+': '[line.split() for line in f]',
			's+d': '[line.split(\';\') for line in f]',
			'ss+': '[[x.strip() for x in line.split()] for line in f]',
			'ss+d': '[[x.strip() for x in line.split(\';\')] for line in f]',
			'r': 'f.read()'}
	with open(filename) as f:
		out = eval(args[style])
	return out