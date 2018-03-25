def get_data(filepath, style=''):
	with open(filepath) as f:
		if style == 'split':
			out = [line.split() for line in f]
		elif style == 'strip':
			out = [line.strip() for line in f]
		elif style == 'bulk':
			out = f.read()
		else:
			out = [line for line in f]
	return out