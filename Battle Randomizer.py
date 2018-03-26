from lib import get_data, message
from random import random, randint

def concat(player, msg):
	return player + ' ' + msg

def roll_dice(prob):
	return 1 if random() < prob else 0

def find(L, ref):
	for i in range(len(L)):
		j = L[i].find(ref)
		if j != -1:
			return i, j
	return -1, -1

def reduce_health(health, player, special):
	health -= 1
	if special == 1:
		health -= 2
	out = ' ' + player + '\'s health is now ' + str(health) + '.'
	return out, health

def do_battle(players, moves, react, rand_act, probs, health):
	side = roll_dice(probs['players'])
	opponent = [p.rnd_msg() for p in players]
	
	if roll_dice(probs['rand_act']) == 1:
		out = concat(opponent[side], rand_act.rnd_msg())
		return out, health
	
	special = roll_dice(probs['special'])
	out = concat(opponent[side], moves[special].rnd_msg())
	
	while roll_dice(probs['counter']) == 1 and special != 1:
		special = roll_dice(probs['special'])
		out += ' Countering, ' + concat(opponent[1-side], moves[special].rnd_msg())
		side = 1-side
	
	outcome = roll_dice(probs['bad'])
	out += ' ' + concat(opponent[1-side], react[outcome][special].rnd_msg())
	
	if outcome == 1:
		a, b = find(players, opponent[1-side])
		temp, health[a][b] = reduce_health(health[a][b], opponent[1-side], special)
		out += temp
	
	return out, health

def main(f):
	pieces = get_data('data_log.txt', 'strip')
	players = [message('data/players_1.txt'), message('data/players_2.txt')]
	moves = [message('data/moves.txt'), message('data/moves_special.txt')]
	react_good = [message('data/reactions_good.txt'), message('data/reactions_good_special.txt')]
	react_bad = [message('data/reactions_bad.txt'), message('data/reactions_bad_special.txt')]
	rand_act = message('data/random_actions.txt')
	raw = get_data('probs.txt', 'split+strip')

	react = [react_good, react_bad]
	probs = {}
	for r in raw:
		probs[r[0]] = float(r[1])
	
	health = [[10, 10, 10], [10]]
	for i in range(len(players)):
		f.write('Side '+ str(i+1) + ': ' + players[i].__str__() + '\n')
		f.write('Health:')
		for h in health[i]:
			f.write(' ' + str(h))
		f.write('\n')
	f.write('\n')
	
	while min(health[0]) > 0 and min(health[1]) > 0:
		out, health = do_battle(players, moves, react, rand_act, probs, health)
		f.write(out + '\n')
	side = 1 if min(health[0]) < min(health[1]) else 2
	f.write('\nSide ' + str(side) + ' is defeated!\n')

with open('result.txt', 'w') as f:
	main(f)