from lib import *
from random import random, randint

def rand_elem(L):
	return L[randint(0, len(L)-1)]

def to_str(L):
	s = ''
	for i in range(len(L)):
		if i > 0:
			s+= ', '
		s += str(L[i])
	return s

def roll_dice(prob):
	return 1 if random() < prob else 0

def find(L, ref):
	for i in range(len(L)):
		for j in range(len(L[i])):
			if L[i][j] == ref:
				return i, j
	return -1, -1

def starting_stats(players, health, f):
	for i in range(len(players)):
		if i > 0:
			f.write('\nv.\n\n')
		for j in range(len(players[i])):
			f.write(players[i][j] + " - health: " + str(health[i][j]) + '\n')
	f.write('\n')

def check_health(health, players, f):
	h = health
	p = players
	indeces = []
	for i in range(len(p)):
		for j in range(len(p[i])):
			if h[i][j] < 1:
				indeces.append((i, j))
	for ix in indeces:
		i, j = ix
		f.write(p[i][j] + ' is too injured and can\'t continue on.\n')
		h[i].pop(j)
		p[i].pop(j)
	return health, players

def reduce_health(health, player, special):
	health -= 1
	if special == 1:
		health -= 2
	out = ' ' + player + '\'s health is now ' + str(health) + '.'
	return out, health

def do_battle(players, moves, react, rand_act, counters, probs, health):
	side = roll_dice(probs['players'])
	opponent = [rand_elem(p) for p in players]
	
	if roll_dice(probs['rand_act']) == 1:
		out = to_str([opponent[side], rand_act.rnd_msg()])
		return out, health
	
	special = roll_dice(probs['special'])
	out = to_str([opponent[side], moves[special].rnd_msg()])
	
	while roll_dice(probs['counter']) == 1 and special != 1:
		special = roll_dice(probs['special'])
		out += ' ' + to_str([counters.rnd_msg(), opponent[1-side], moves[special].rnd_msg()])
		side = 1-side
	
	outcome = roll_dice(probs['bad'])
	out += ' ' + to_str([opponent[1-side], react[outcome][special].rnd_msg()])
	
	if outcome == 1:
		a, b = find(players, opponent[1-side])
		temp, health[a][b] = reduce_health(health[a][b], opponent[1-side], special)
		out += temp
	
	return out, health
	
def main(f):
	pieces = get_data('data_log.txt', 's')
	raw = [get_data('data/players_1.txt', 'ss+d'), get_data('data/players_2.txt', 'ss+d')]
	[[print(p) for p in r] for r in raw]
	players = [[p[0] for p in r] for r in raw]
	health = [[int(h[1]) for h in r] for r in raw]
	
	moves = [message('data/moves.txt'), message('data/moves_special.txt')]
	react_good = [message('data/reactions_good.txt'), message('data/reactions_good_special.txt')]
	react_bad = [message('data/reactions_bad.txt'), message('data/reactions_bad_special.txt')]
	react = [react_good, react_bad]
	rand_act = message('data/random_actions.txt')
	counters = message('data/counters.txt')
	
	player_ref = [to_str(p) for p in players]
	
	raw = get_data('probs.txt', 'ss+')
	probs = {}
	for r in raw:
		probs[r[0]] = float(r[1])
	
	starting_stats(players, health, f)
	
	while len(health[0]) > 0 and len(health[1]) > 0:
		out, health = do_battle(players, moves, react, rand_act, counters, probs, health)
		f.write(out + '\n')
		health, players = check_health(health, players, f)
	side = 0 if len(health[0]) == 0 else 1
	f.write(to_str(players[1-side]) + ' defeated ' + player_ref[side] + '!\n')

class forDebugging:
	def write(self, arg):
		print(arg)

#with open('result.txt', 'w') as f:
f = forDebugging()
main(f)

''' TODO:
		allow move damage to be customized (msg overhaul needed)'''