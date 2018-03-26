from lib import *
from random import random, randint

def rand_elem(L):
	return L[randint(0, len(L)-1)]

def to_str(L, ch=','):
	s = ''
	for i in range(len(L)):
		if i > 0:
			s+= ch + ' '
		s += str(L[i])
	return s

def roll_dice(prob):
	return 1 if random() < prob else 0

def findMsg(M, msg):
	for i in range(len(M)):
		j = M[i].find(msg)
		if j != -1:
			return i, j
	return -1, -1

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
		f.write(p[i][j] + ' is too injured and can\'t continue on.\n\n')
		h[i].pop(j)
		p[i].pop(j)
	return health, players

def reduce_health(health, damage, player, special):
	health -= damage
	out = ' ' + player + '\'s health is now ' + str(health) + '.'
	return out, health

def do_battle(players, moves, react, rand_act, counters, probs, health, dmg):
	side = roll_dice(probs['players'])
	opponent = [rand_elem(p) for p in players]
	
	if roll_dice(probs['rand_act']) == 1:
		out = to_str([opponent[side], rand_act.rnd_msg()], '')
		return out, health
	
	special = roll_dice(probs['special'])
	move = moves[special].rnd_msg()
	out = to_str([opponent[side], move], '')
	
	while roll_dice(probs['counter']) == 1 and special != 1:
		special = roll_dice(probs['special'])
		move = moves[special].rnd_msg()
		out += ' ' + to_str([counters.rnd_msg(), opponent[1-side], move], '')
		side = 1-side
	
	outcome = roll_dice(probs['bad'])
	out += ' ' + to_str([opponent[1-side], react[outcome][special].rnd_msg()], '')
	
	if outcome == 1:
		a, b = find(players, opponent[1-side])
		c, d = findMsg(moves, move)
		temp, health[a][b] = reduce_health(health[a][b], dmg[c][d], opponent[1-side], special)
		out += temp
	
	return out, health
	
def main(f):
	pieces = get_data('data_log.txt', 's')
	
	raw = [get_data('data/players_1.txt', 'ss+d'), get_data('data/players_2.txt', 'ss+d')]
	players = [[p[1] for p in r] for r in raw]
	health = [[float(h[0]) for h in r] for r in raw]
	player_ref = [to_str(p) for p in players]
	
	raw = [get_data('data/moves.txt', 'ss+d'), get_data('data/moves_special.txt', 'ss+d')]
	moves = [message('', [m[1] for m in r]) for r in raw]
	dmg = [[float(d[0]) for d in r] for r in raw]
	
	react_good = [message('data/reactions_good.txt'), message('data/reactions_good_special.txt')]
	react_bad = [message('data/reactions_bad.txt'), message('data/reactions_bad_special.txt')]
	react = [react_good, react_bad]
	rand_act = message('data/random_actions.txt')
	counters = message('data/counters.txt')
	
	raw = get_data('probs.txt', 'ss+')
	probs = {}
	for r in raw:
		probs[r[0]] = float(r[1])
	
	starting_stats(players, health, f)
	
	while len(health[0]) > 0 and len(health[1]) > 0:
		out, health = do_battle(players, moves, react, rand_act, counters, probs, health, dmg)
		f.write(out + '\n')
		health, players = check_health(health, players, f)
	side = 0 if len(health[0]) == 0 else 1
	f.write(to_str(players[1-side]) + ' defeated ' + player_ref[side] + '!\n')

'''class forDebugging:
	def write(self, arg):
		print(arg)
f = forDebugging()'''
with open('result.txt', 'w') as f:
	main(f)