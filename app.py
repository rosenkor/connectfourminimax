from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from minimax.program import connect_four_ab

import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.get_json()
    logging.debug("Received data: %s", data)  # Log the incoming JSON data
    contents = data['contents']
    turn = data['turn']
    max_depth = 5
    best_column = connect_four_ab(contents, turn, max_depth)
    return jsonify({'bestMove': best_column})

@app.route('/minimax/__init__.py')
def serve_minimax_init():
    minimax_dir = os.path.join(app.root_path, 'minimax')
    return send_from_directory(minimax_dir, '__init__.py')

@app.route('/minimax/program.py')
def serve_minimax_program():
    minimax_dir = os.path.join(app.root_path, 'minimax')
    return send_from_directory(minimax_dir, 'program.py')

@app.route('/minimax/true_ab.py')
def serve_minimax_true_ab():
    minimax_dir = os.path.join(app.root_path, 'minimax')
    return send_from_directory(minimax_dir, 'true_ab.py')

@app.route('/static/script.py')
def serve_static_script():
    static_dir = os.path.join(app.root_path, 'static')
    return send_from_directory(static_dir, 'script.py')

@app.route('/minimax/helper_functions.py')
def serve_minimax_helper_functions():
    minimax_dir = os.path.join(app.root_path, 'minimax')
    return send_from_directory(minimax_dir, 'helper_functions.py')

# Add similar routes for other files in the minimax package

if __name__ == '__main__':
    app.run()