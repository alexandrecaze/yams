from flask import Flask, request, render_template
import json
import pandas as pd
import numpy as np
app = Flask(__name__)

DICE_MAPPING =	{1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

@app.route('/')
def hello_world():
    dice_state = np.random.randint(1, 7, 5)
    dice_values = [DICE_MAPPING[dice] for dice in dice_state]
    player_names = ['Alex', 'Nico']
    coups = ['1', '2', '3', '4', '5', '6', 'Min', 'Max', 'Brelan', 'Carré', 'Pte suite', 'Gde suite', 'Yams', 'Bonus', 'Total']
    scores = pd.DataFrame(data=np.zeros((len(coups), len(player_names)), dtype=int), columns=player_names, index=coups)
    return render_template('server.html', dice_values=dice_values, player_names=player_names, coups=coups, scores=scores.to_html(classes=["table", "table-sm"], border=0, justify='left'))


def is_yams(die_state):
    return len(set(die_state)) == 1

def compute_proba_yams_one_throw(selected_die):
    die_to_throw = np.sum([s is None for s in selected_die])
    die_to_keep = [die + 1 for die in selected_die if die is not None]
    N_MONTECARLO = 10000
    res = np.zeros((N_MONTECARLO, 5))
    res[:, :len(die_to_keep)] = die_to_keep
    res[:, len(die_to_keep):] = np.random.randint(0, 6, (N_MONTECARLO, die_to_throw))
    proba = (pd.DataFrame(res).nunique(axis=1) == 1).mean()
    return proba

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_data()
    data = json.loads(data)
    selected_die = data['selectedDie']
    proba = compute_proba_yams_one_throw(selected_die)
    return json.dumps({'proba_yams_one_throw': 100 * proba})

if __name__ == '__main__':
  app.run()
