import numpy as np
import os
import pandas as pd
import re


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
		yams=None):
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
		+ coalesce(self.yams)

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
		if self.numbers[0] is not None:
			possible_scores['[1] Ones'] = (dice_state == 1).astype(int).sum()
		if self.numbers[1] is not None:
			possible_scores['[2] Twos'] = (dice_state == 2).astype(int).sum() * 2
		# 	'[3] Threes': (dice_state == 3).astype(int).sum() * 3,
		# 	'[4] Fours': (dice_state == 4).astype(int).sum() * 4,
		# 	'[5] Fives': (dice_state == 5).astype(int).sum() * 5,
		# 	'[6] Sixes': (dice_state == 6).astype(int).sum() * 6,
		# 	'[7] Minimum': dice_state.sum(),
		# 	'[8] Maximum': dice_state.sum(),
		# 	'[9] Brelan': dice_state.sum() if self.is_brelan(dice_state) else 0,
		# 	'[10] Full': 25 if len(set(dice_state)) == 2 and (dice_state == dice_state[0]).sum() in [2, 3] else 0,
		# 	'[11] Square': dice_state.sum() if self.is_square(dice_state) else 0,
		# 	'[12] Little suite': 30 if set(dice_state) in [
		# 		{1, 2, 3, 4},
		# 		{2, 3, 4, 5},
		# 		{3, 4, 5, 6},
		# 		{1, 2, 3, 4, 6},
		# 		{1, 3, 4, 5, 6},
		# 		{1, 2, 3, 4, 5},
		# 		{2, 3, 4, 5, 6},
		# 	] else 0,
		# 	'[13] Big suite': 40 if set(dice_state) in [
		# 		{1, 2, 3, 4, 5},
		# 		{2, 3, 4, 5, 6},
		# 	] else 0,
		# 	'[14] Yams': 50 if len(set(dice_state)) == 1 else 0,
		# }

	def display_possible_scores(self, dice_state):
		print('Possible scores:')
		for key, value in self.possible_scores(dice_state.copy()).items():
			print(key, value)


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
		self.display_possible_scores(dice_state)
		input()
		

class Game(object):

	def __init__(self, player_names=['Billy', 'Joel']):
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