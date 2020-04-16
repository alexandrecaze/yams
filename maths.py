import pandas as pd
import numpy as np

DICE_MAPPING =	{1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
COUPS = {
    'One one': 1, 'Two ones': 2, 'Three ones': 3, 'Four ones': 4, 'Five ones': 5,
    'One two': 2, 'Two twos': 4, 'Three twos': 6, 'Four twos': 8, 'Five twos': 10,
    'One three': 3, 'Two threes': 6, 'Three threes': 9, 'Four threes': 12, 'Five threes': 15,
    'One four': 4, 'Two fours': 8, 'Three fours': 12, 'Four fours': 16, 'Five fours': 20,
    'One five': 5, 'Two fives': 10, 'Three fives': 15, 'Four fives': 20, 'Five fives': 25,
    'One six': 6, 'Two sixes': 12, 'Three sixes': 18, 'Four sixes': 24, 'Five sixes': 30,
    'Little suite': 30, 'Big suite': 40, 'Brelan': None, 'Full': 25, 'Square': None, 'Yams': 50,
}


def simulate_next_throw(selected_die, n_montecarlo=1000):
    die_to_throw = np.sum([s is None for s in selected_die])
    die_to_keep = [die + 1 for die in selected_die if die is not None]
    throws = np.zeros((n_montecarlo, 5))
    throws[:, :len(die_to_keep)] = die_to_keep
    throws[:, len(die_to_keep):] = np.random.randint(1, 7, (n_montecarlo, die_to_throw))
    return throws


def compute_probas(selected_die):
    next_throw_simulations = simulate_next_throw(selected_die, 10000)
    successes = check_for_success(next_throw_simulations)
    df_probas = pd.DataFrame({'coups': list(COUPS.keys()), 'proba': np.around(successes.mean(axis=0), decimals=2)})
    df_probas['points'] = compute_points(next_throw_simulations, successes)
    df_probas['esperance'] = df_probas['proba'] * df_probas['points']
    return df_probas[df_probas.proba>0].sort_values(by='esperance', ascending=False)


def compute_points(throws, successes):
    scores = np.zeros(successes.shape)
    final_score = np.zeros(36)

    for x in range(6):
        scores[:, x * 5] = (x + 1) * successes[:, x * 5]
        scores[:, x * 5 + 1] = 2 * (x + 1) * successes[:, x * 5 + 1]
        scores[:, x * 5 + 2] = 3 * (x + 1) * successes[:, x * 5 + 2]
        scores[:, x * 5 + 3] = 4 * (x + 1) * successes[:, x * 5 + 3]
        scores[:, x * 5 + 4] = 5 * (x + 1) * successes[:, x * 5 + 4]
    scores[:, 30] = 30 * successes[:, 30] # petite suite
    scores[:, 31] = 40 * successes[:, 31] # grande suite
    scores[:, 33] = 25 * successes[:, 33] # full
    scores[:, 35] = 50 * successes[:, 35] # yams
    scores[:, 32] = throws.sum(axis=1) * successes[:, 32] # brelan
    scores[:, 34] = throws.sum(axis=1) * successes[:, 34] # carré
    for x in range(36):
        if successes[:, x].sum() != 0:
            final_score[x] = round((scores[:, x].sum() / successes[:, x].sum()), 1)
    return final_score


def check_for_success(throws):
    df_throws = pd.DataFrame(throws)
    sets_of_throws = np.array([set(l) for l in df_throws.values])

    df_counts = pd.DataFrame(columns=['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'])
    df_counts['twos'] = (df_throws == 2).sum(axis=1)
    df_counts['ones'] = (df_throws == 1).sum(axis=1)
    df_counts['threes'] = (df_throws == 3).sum(axis=1)
    df_counts['fours'] = (df_throws == 4).sum(axis=1)
    df_counts['fives'] = (df_throws == 5).sum(axis=1)
    df_counts['sixes'] = (df_throws == 6).sum(axis=1)
    sets_of_counts = np.array([set(l) for l in df_counts.values])

    successes = np.zeros((throws.shape[0], 36))
    # Yams
    successes[:, 35] = (df_counts >= 5).any(axis=1)
    # Square
    successes[:, 34] = (df_counts >= 4).any(axis=1)
    # Full
    successes[:, 33] = sets_of_counts == {0, 2, 3}
    # Brelan
    successes[:, 32] = (df_counts >= 3).any(axis=1)
    # Big suite
    successes[:, 31] = np.isin(sets_of_throws, [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}])
    # Little suite
    successes[:, 30] = np.isin(sets_of_throws, [
        {1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6},
        {1, 2, 3, 4, 6}, {1, 3, 4, 5, 6},
        {1, 2, 3, 4, 5}, {2, 3, 4, 5, 6},
    ])
    # Sixes
    successes[:, 29] = df_counts['sixes'] == 5
    successes[:, 28] = df_counts['sixes'] >= 4
    successes[:, 27] = df_counts['sixes'] >= 3
    successes[:, 26] = df_counts['sixes'] >= 2
    successes[:, 25] = df_counts['sixes'] >= 1
    # Fives
    successes[:, 24] = df_counts['fives'] == 5
    successes[:, 23] = df_counts['fives'] >= 4
    successes[:, 22] = df_counts['fives'] >= 3
    successes[:, 21] = df_counts['fives'] >= 2
    successes[:, 20] = df_counts['fives'] >= 1
    # Fours
    successes[:, 19] = df_counts['fours'] == 5
    successes[:, 18] = df_counts['fours'] >= 4
    successes[:, 17] = df_counts['fours'] >= 3
    successes[:, 16] = df_counts['fours'] >= 2
    successes[:, 15] = df_counts['fours'] >= 1
    # Threes
    successes[:, 14] = df_counts['threes'] == 5
    successes[:, 13] = df_counts['threes'] >= 4
    successes[:, 12] = df_counts['threes'] >= 3
    successes[:, 11] = df_counts['threes'] >= 2
    successes[:, 10] = df_counts['threes'] >= 1
    # Twos
    successes[:, 9] = df_counts['twos'] == 5
    successes[:, 8] = df_counts['twos'] >= 4
    successes[:, 7] = df_counts['twos'] >= 3
    successes[:, 6] = df_counts['twos'] >= 2
    successes[:, 5] = df_counts['twos'] >= 1
    # One
    successes[:, 4] = df_counts['ones'] == 5
    successes[:, 3] = df_counts['ones'] >= 4
    successes[:, 2] = df_counts['ones'] >= 3
    successes[:, 1] = df_counts['ones'] >= 2
    successes[:, 0] = df_counts['ones'] >= 1
    return successes


THROWS = np.array([
    [1, 1, 1, 1, 1], # Yams
    [6, 6, 6, 6, 6], # Yams
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