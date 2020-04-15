from flask import Flask, request, render_template
import json
import pandas as pd
import numpy as np

from maths import compute_probas

app = Flask(__name__)

@app.route('/')
def server():
    return render_template('server.html')

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_data()
    data = json.loads(data)
    df_probas = compute_probas(data['selectedDie'])
    return json.dumps({'df_probas': df_probas.to_html(index=False, border=0)})

if __name__ == '__main__':
  app.run()
