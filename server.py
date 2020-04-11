from flask import Flask, request, render_template
import json
import numpy as np
app = Flask(__name__)

DICE_MAPPING =	{1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

@app.route('/')
def hello_world():
    dice_state = np.random.randint(1, 7, 5)
    dice_values = [DICE_MAPPING[dice] for dice in dice_state]
    player_names = ['Alex', 'Nico']
    coups = ['1', '2', '3', '4', '5', '6', 'Bonus', 'Min', 'Max', 'Brelan', 'Carré', 'Pte suite', 'Gde suite', 'Yams']
    scores = np.zeros((len(coups), len(player_names)))
    print(coups)
    print(player_names)
    print(scores)
    return render_template('server.html', dice_values=dice_values, player_names=player_names, coups=coups, scores=scores)

@app.route('/compute', methods=['POST'])
def compute():
	data = request.get_data()
	print(json.loads(data))
	return json.dumps({'coucou': 'toi'})

if __name__ == '__main__':
  app.run()
