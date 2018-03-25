from file_access import get_data
from random import randint, random

def toStr(L):
	out = ''
	for i in range(len(L)):
		if i > 0:
			out += ' '
		out += str(L[i])
	return out

def argmin(L):
	m = L[0]
	index = 0
	for i in range(1, len(L)):
		if m > L[i]:
			m = L[i]
			index = i
	return index;

def load_data():
	pieces = get_data('data_log.txt', 'strip')
	data = [get_data('data/' + file + '.txt', 'strip') for file in pieces]
	for d in data:
		for x in d:
			x.strip()

	raw = get_data('probs.txt', 'split')
	mod_probs = [float(raw[i][1]) for i in range(len(raw))]
	probs = [len(data[i])/mod_probs[i] for i in range(len(data))]
	probs = probs + [mod_probs[i] for i in range(len(data), len(mod_probs))]
	
	return data, probs

def do_battle(data, probs, health, f):
	f.write(toStr(data[0]) + '\n')
	f.write(toStr(health) + '\n')
	while(min(health) > 0):
		outcome = [randint(0, probs[i]-1) for i in range(len(probs)-2)]
		second_index = (outcome[0]+1)%len(data[0])
		persons = [data[0][outcome[0]], data[0][second_index]]
		
		k = 0 if random() > probs[5] else 2
		out = persons[0] + ' ' + data[1+k][outcome[1+k]] + '.'
		bool = True
		while(random() < probs[6]):
			i = 1 if bool else 0
			out += ' Countering, ' + persons[i] + ' ' + data[1+k][randint(0, probs[1+k]-1)] + '.'
			bool = not bool
		
		i = 1 if bool else 0
		out += ' ' + persons[i] + ' ' + data[2+k][outcome[2+k]] + '.'
		f.write(out + '\n')
		
		if outcome[2+k] == 0:
			health[outcome[0]]-=k+1
			f.write(toStr(health) + '\n')
	
	f.write(data[0][argmin(health)] + ' is defeated!\n')
	
def main(f):
	data, probs = load_data()
	health = [5 for _ in range(len(data[0]))]
	do_battle(data, probs, health, f)
with open('result.txt', 'w') as f:
	main(f)