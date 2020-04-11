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
    coups = ['1', '2', '3', '4', '5', '6', 'Bonus', 'Min', 'Max', 'Brelan', 'Carré', 'Pte suite', 'Gde suite', 'Yams']
    scores = pd.DataFrame(data=np.zeros((len(coups), len(player_names)), dtype=int), columns=player_names, index=coups)
    return render_template('server.html', dice_values=dice_values, player_names=player_names, coups=coups, scores=scores.to_html(classes=["table", "table-sm"], border=0, justify='left'))

@app.route('/compute', methods=['POST'])
def compute():
	data = request.get_data()
	print(json.loads(data))
	return json.dumps({'coucou': 'toi'})

if __name__ == '__main__':
  app.run()
