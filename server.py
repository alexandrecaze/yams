from flask import Flask, render_template
import numpy as np
app = Flask(__name__)

DICE_MAPPING =	{1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

@app.route('/')
def hello_world():
    dice_state = np.random.randint(1, 7, 5)
    dice_values = [DICE_MAPPING[dice] for dice in dice_state]
    return render_template('server.html', dice_values=dice_values)

if __name__ == '__main__':
  app.run()
