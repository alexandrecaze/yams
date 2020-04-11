import numpy as np
import os
import pandas as pd
import re

DISPLAY_NAMES = {
	1: '[1] Ones',
	2: '[2] Twos',
	3: '[3] Threes',
	4: '[4] Fours',
	5: '[5] Fives',
	6: '[6] Sixes',
	7: '[7] Minimum',
	8: '[8] Maximum',
	9: '[9] Brelan',
	10: '[10] Full',
	11: '[11] Square',
	12: '[12] Little suite',
	13: '[13] Big suite',
	14: '[14] Yams',	
	15: '[15] Chance',
}

def clear_and_print(coucou):
	os.system('clear')
	print(coucou)

def coalesce(value):
	return int(value or 0)

class Player(object):

	def __init__(
		self, 
		name='Billy',
		numbers=np.array([None, None, None, None, None, None]),
		minimum=None,
		maximum=None,
		brelan=None,
		little_suite=None,
		big_suite=None,
		full=None,
		square=None,
		yams=None,
		chance=None):
		self.name = name
		self.numbers = numbers
		self.minimum = minimum
		self.maximum = maximum
		self.brelan = brelan
		self.little_suite = little_suite
		self.big_suite = big_suite
		self.full = full
		self.square = square
		self.yams = yams
		self.chance = chance

	def __str__(self):
		return self.name

	@property
	def score(self):
		return pd.Series(self.numbers).fillna(0).sum() \
		+ coalesce(self.minimum) \
		+ coalesce(self.maximum) \
		+ coalesce(self.brelan) \
		+ coalesce(self.little_suite) \
		+ coalesce(self.big_suite) \
		+ coalesce(self.full) \
		+ coalesce(self.square) \
		+ coalesce(self.yams) \
		+ coalesce(self.chance)

	@property
	def bonus(self):
		return (sum(self.numbers) >= 63) * 35

	def score_number(self, number, count):
		self.numbers[number - 1] = count * number

	def score_minimum(self, score):
		self.minimum = score
 
	def score_maximum(self, score):
		self.maximum = score

	def score_brelan(self, score):
		self.brelan = score

	def score_square(self, score):
		self.square = score

	def score_little_suite(self):
		self.little_suite = 30

	def score_big_suite(self):
		self.big_suite = 40

	def score_full(self):
		self.big_suite = 25
	
	def score_yams(self):
		self.yams = 50

	def score_chance(self, score):
		self.chance = score

	def chose(self):
		choice = ''
		while not re.match(r'^[kt]{5}$', choice):
			choice = input('k to keep and t to throw. Example: kktkk\n')
		return choice

	def throw(self, choice='ttttt', dice_state=np.zeros(3)):
		if dice_state.sum() == 0:
			return np.random.randint(1, 7, 5)
		else:
			for i in range(len(choice)):
				if choice[i] == 't':
					dice_state[i] = np.random.randint(1, 7)
			return dice_state

	def is_brelan(self, dice_state):
		values = set(dice_state)
		for value in values:
			if (dice_state == value).astype(int).sum() >= 3:
				return True
		return False

	def is_square(self, dice_state):
		values = set(dice_state)
		for value in values:
			if (dice_state == value).astype(int).sum() >= 4:
				return True
		return False

	def possible_scores(self, dice_state):
		dice_state.sort()
		possible_scores = {}
		if self.numbers[0] is None:
			possible_scores[DISPLAY_NAMES[1]] = (dice_state == 1).astype(int).sum()
		if self.numbers[1] is None:
			possible_scores[DISPLAY_NAMES[2]] = (dice_state == 2).astype(int).sum() * 2
		if self.numbers[2] is None:
			possible_scores[DISPLAY_NAMES[3]] = (dice_state == 3).astype(int).sum() * 3
		if self.numbers[3] is None:
			possible_scores[DISPLAY_NAMES[4]] = (dice_state == 4).astype(int).sum() * 4
		if self.numbers[4] is None:
			possible_scores[DISPLAY_NAMES[5]] = (dice_state == 5).astype(int).sum() * 5
		if self.numbers[5] is None:
			possible_scores[DISPLAY_NAMES[6]] = (dice_state == 6).astype(int).sum() * 6
		if self.minimum is None:
			possible_scores[DISPLAY_NAMES[7]] = dice_state.sum()
		if self.maximum is None:
			possible_scores[DISPLAY_NAMES[8]] = dice_state.sum()
		if self.brelan is None:
			possible_scores[DISPLAY_NAMES[9]] = dice_state.sum() if self.is_brelan(dice_state) else 0
		if self.full is None:
			possible_scores[DISPLAY_NAMES[10]] = 25 if len(set(dice_state)) == 2 and (dice_state == dice_state[0]).sum() in [2, 3] else 0
		if self.square is None:
			possible_scores[DISPLAY_NAMES[11]] = dice_state.sum() if self.is_square(dice_state) else 0
		if self.little_suite is None:
			possible_scores[DISPLAY_NAMES[12]] = 30 if set(dice_state) in [
				{1, 2, 3, 4},
				{2, 3, 4, 5},
				{3, 4, 5, 6},
				{1, 2, 3, 4, 6},
				{1, 3, 4, 5, 6},
				{1, 2, 3, 4, 5},
				{2, 3, 4, 5, 6},
			] else 0
		if self.big_suite is None:
			possible_scores[DISPLAY_NAMES[13]] = 40 if set(dice_state) in [
				{1, 2, 3, 4, 5},
				{2, 3, 4, 5, 6},
			] else 0
		if self.yams is None:
			possible_scores[DISPLAY_NAMES[14]] = 50 if len(set(dice_state)) == 1 else 0
		if self.chance is None:
			possible_scores[DISPLAY_NAMES[15]] = dice_state.sum()
		return possible_scores

	def display_possible_scores(self, dice_state, chose=False):
		print('Possible scores:')
		possible_scores = self.possible_scores(dice_state.copy())
		for key, value in possible_scores.items():
			print(key, value)
		if chose:
			choice = input('What\'s it gonna be ?')
			print(choice)
			import pdb
			pdb.set_trace()

	def play(self):
		clear_and_print('======')
		input('It is {name}\'s turn to play. Go ?'.format(name=self.name))
		dice_state = self.throw()
		print(dice_state)
		self.display_possible_scores(dice_state)
		choice = self.chose()
		print(choice)
		print('{name}: throw 2:'.format(name=self.name))
		dice_state = self.throw(choice, dice_state)
		print(dice_state)
		self.display_possible_scores(dice_state)
		choice = self.chose()
		print(choice)
		print('{name}: Final throw:'.format(name=self.name))
		dice_state = self.throw(choice, dice_state)
		clear_and_print(dice_state)
		self.display_possible_scores(dice_state, chose=True)
		input()
		

class Game(object):

	def __init__(self, player_names=['Billy']):
		self.players = [Player(player_name) for player_name in player_names]
		self.throws = {player.name: np.zeros((14, 5)) for player in self.players}
		self.play_count = 0

	@property
	def scores(self):
		'''
		Returns each player's score.
		'''
		return {player.name: player.score for player in self.players}

	def print_scores(self):
		print('Here are the scores:')
		print(self.scores)

	def start(self):
		for player in self.players:
			print('Hello {name}'.format(name=player.name))
		self.print_scores()
		for turn in range(14):
			for player in self.players:
				player.play()
				break


if __name__ == '__main__':
	g = Game()
	g.start()
