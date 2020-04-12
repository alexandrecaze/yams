import pandas as pd
import numpy as np


def check_for_success(throws):
	df_throws = pd.DataFrame(throws)
	sets_of_throws = np.array([set(l) for l in df_throws.values])

	df_counts = pd.DataFrame(columns=['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'])
	df_counts['ones'] = (df_throws == 1).sum(axis=1)
	df_counts['twos'] = (df_throws == 2).sum(axis=1)
	df_counts['threes'] = (df_throws == 3).sum(axis=1)
	df_counts['fours'] = (df_throws == 4).sum(axis=1)
	df_counts['fives'] = (df_throws == 5).sum(axis=1)
	df_counts['sixes'] = (df_throws == 6).sum(axis=1)
	sets_of_counts = np.array([set(l) for l in df_counts.values])

	res = np.zeros((throws.shape[0], 36))
	# Yams
	res[:, 35] = (df_counts >= 5).any(axis=1)
	# Square
	res[:, 34] = (df_counts >= 4).any(axis=1)
	# Full
	res[:, 33] = sets_of_counts == {0, 2, 3}
	# Brelan
	res[:, 32] = (df_counts >= 3).any(axis=1)
	# Big suite
	res[:, 31] = np.isin(sets_of_throws, [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}])
	# Little suite
	res[:, 30] = np.isin(sets_of_throws, [
		{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6},
		{1, 2, 3, 4, 6}, {1, 3, 4, 5, 6},
		{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6},
	])
	# Sixes
	res[:, 29] = df_counts['sixes'] == 5
	res[:, 28] = df_counts['sixes'] >= 4
	res[:, 27] = df_counts['sixes'] >= 3
	res[:, 26] = df_counts['sixes'] >= 2
	res[:, 25] = df_counts['sixes'] >= 1
	# Fives
	res[:, 24] = df_counts['fives'] == 5
	res[:, 23] = df_counts['fives'] >= 4
	res[:, 22] = df_counts['fives'] >= 3
	res[:, 21] = df_counts['fives'] >= 2
	res[:, 20] = df_counts['fives'] >= 1
	# Fours
	res[:, 19] = df_counts['fours'] == 5
	res[:, 18] = df_counts['fours'] >= 4
	res[:, 17] = df_counts['fours'] >= 3
	res[:, 16] = df_counts['fours'] >= 2
	res[:, 15] = df_counts['fours'] >= 1
	# Threes
	res[:, 14] = df_counts['threes'] == 5
	res[:, 13] = df_counts['threes'] >= 4
	res[:, 12] = df_counts['threes'] >= 3
	res[:, 11] = df_counts['threes'] >= 2
	res[:, 10] = df_counts['threes'] >= 1
	# Twos
	res[:, 9] = df_counts['twos'] == 5
	res[:, 8] = df_counts['twos'] >= 4
	res[:, 7] = df_counts['twos'] >= 3
	res[:, 6] = df_counts['twos'] >= 2
	res[:, 5] = df_counts['twos'] >= 1
	# One
	res[:, 4] = df_counts['ones'] == 5
	res[:, 3] = df_counts['ones'] >= 4
	res[:, 2] = df_counts['ones'] >= 3
	res[:, 1] = df_counts['ones'] >= 2
	res[:, 0] = df_counts['ones'] >= 1
	return res


THROWS = np.array([
	[1, 1, 1, 1, 1], 
	[6, 6, 6, 6, 6], 
	[2, 2, 3, 2, 2], # Square
	[1, 4, 4, 4, 4], # Square
	[5, 1, 4, 5, 5], # Brelan
	[2, 1, 2, 5, 2], # Brelan
	[3, 2, 3, 3, 2], # Brelan
	[3, 2, 3, 3, 3], # Brelan
	[1, 2, 1, 2, 1], # Full
	[4, 4, 5, 5, 5], # Full
	[1, 2, 3, 4, 5], # Gde suite
	[6, 2, 3, 4, 5], # Gde suite
	[1, 2, 4, 3, 1], # Pte suite
	[5, 2, 3, 4, 2], # Pte suite
	[6, 5, 3, 4, 4], # Pte suite
	[1, 3, 2, 1, 1], # Three ones
	[2, 2, 2, 2, 2], # Five twos
	[3, 3, 2, 1, 2], # Two threes
	[1, 5, 5, 3, 6], # Zero fours
	[5, 6, 5, 5, 4], # Three fives
	[6, 2, 5, 3, 4], # One six
	[3, 1, 4, 2, 2], # Minimum is 12
	[6, 3, 5, 4, 6], # Maximum is 24
])

THROWS_SUCCESS = np.array([
	# [1, 1, 1, 1, 1] Yams
	[
		True, True, True, True, True, # Ones
		False, False, False, False, False, # Twos
		False, False, False, False, False, # Threes
		False, False, False, False, False, # Fours
		False, False, False, False, False, # Fives
		False, False, False, False, False, # Sixes
		False, False, True, False, True, True, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [6, 6, 6, 6, 6] Yams
	[
		False, False, False, False, False, # Ones
		False, False, False, False, False, # Twos
		False, False, False, False, False, # Threes
		False, False, False, False, False, # Fours
		False, False, False, False, False, # Fives
		True, True, True, True, True, # Sixes
		False, False, True, False, True, True, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [2, 2, 3, 2, 2] # Square
	[
		False, False, False, False, False,
		True, True, True, True, False,
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, True, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 4, 4, 4, 4] Square
	[
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, True, True, True, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, True, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [5, 1, 4, 5, 5] Brelan
	[
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		True, True, True, False, False,
		False, False, False, False, False,
		False, False, True, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [2, 1, 2, 5, 2] Brelan
	[
		True, False, False, False, False,
		True, True, True, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [3, 2, 3, 3, 2] Brelan
	[
		False, False, False, False, False,
		True, True, False, False, False,
		True, True, True, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, True, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [3, 2, 3, 3, 3] Brelan
	[
		False, False, False, False, False,
		True, False, False, False, False,
		True, True, True, True, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, True, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 2, 1, 2, 1] Full
	[
		True, True, True, False, False,
		True, True, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, True, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [4, 4, 5, 5, 5] Full
	[
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, True, False, False, False,
		True, True, True, False, False,
		False, False, False, False, False,
		False, False, True, True, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 2, 3, 4, 5] Gde suite
	[
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		True, True, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [6, 2, 3, 4, 5] Gde suite
	[
		False, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, True, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 2, 4, 3, 1] Pte suite
	[
		True, True, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [5, 2, 3, 4, 2] Pte suite
	[
		False, False, False, False, False,
		True, True, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [6, 5, 3, 4, 4] Pte suite
	[
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		True, True, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 3, 2, 1, 1] Three ones
	[
		True, True, True, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [2, 2, 2, 2, 2] Five twos
	[
		False, False, False, False, False,
		True, True, True, True, True,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, True, False, True, True, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [3, 3, 2, 1, 2] Two threes
	[
		True, False, False, False, False,
		True, True, False, False, False,
		True, True, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [1, 5, 5, 3, 6] Zero fours
	[
		True, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		True, True, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [5, 6, 5, 5, 4] Three fives
	[
		False, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		True, True, True, False, False,
		True, False, False, False, False,
		False, False, True, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [6, 2, 5, 3, 4] One six
	[
		False, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, True, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [3, 1, 4, 2, 2] Minimum is 12
	[
		True, False, False, False, False,
		True, True, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
	# [6, 3, 5, 4, 6] Maximum is 2
	[
		False, False, False, False, False,
		False, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, False, False, False, False,
		True, True, False, False, False,
		True, False, False, False, False, False, # Little suite, Big suite, Brelan, Full, Square, Yams
	],
])


def test_check_for_success():
	# Those values allow to debug by dichotomy
	COUPS_MIN, COUPS_MAX = 0, 36
	THROWS_MIN, THROWS_MAX = 0, 23
	if (len(THROWS) != THROWS_MAX):
		raise ValueError('Wesh')
	np.testing.assert_array_equal(
		check_for_success(THROWS)[THROWS_MIN:THROWS_MAX, COUPS_MIN:COUPS_MAX], 
		THROWS_SUCCESS[THROWS_MIN:THROWS_MAX, COUPS_MIN:COUPS_MAX]
	)