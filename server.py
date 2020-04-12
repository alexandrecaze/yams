from flask import Flask, request, render_template
import json
import pandas as pd
import numpy as np

from check_for_success import check_for_success

app = Flask(__name__)

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

@app.route('/')
def hello_world():
    return render_template('probas.html')

def simulate_next_throw(selected_die, n_montecarlo=1000):
    die_to_throw = np.sum([s is None for s in selected_die])
    die_to_keep = [die + 1 for die in selected_die if die is not None]
    res = np.zeros((n_montecarlo, 5))
    res[:, :len(die_to_keep)] = die_to_keep
    res[:, len(die_to_keep):] = np.random.randint(0, 6, (n_montecarlo, die_to_throw))
    return res

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_data()
    data = json.loads(data)
    selected_die = data['selectedDie']
    next_throw_simulations = simulate_next_throw(selected_die, 10000)
    probas = check_for_success(next_throw_simulations)
    df_probas = pd.DataFrame({'': list(COUPS.keys()), 'proba': probas.mean(axis=0)})
    df_probas['points'] = df_probas[''].map(COUPS)
    df_probas['esperance'] = df_probas['proba'] * df_probas['points']
    return json.dumps({'df_probas': df_probas[df_probas.proba>0].sort_values(by='esperance', ascending=False).to_html(index=False, border=0)})

if __name__ == '__main__':
  app.run()
