def get_data(filename, style):
	args = {'': '[line for line in f]',
			'strip': '[line.strip() for line in f]',
			'split': '[line.split() for line in f]',
			'split_delim': '[line.split(\':\') for line in f]',
			'split+strip': '[[x.strip() for x in line.split()] for line in f]',
			'strip+split': '[[x.strip() for x in line.split()] for line in f]',
			'raw': 'f.read()'}
	with open(filename) as f:
		out = eval(args[style])
	return out