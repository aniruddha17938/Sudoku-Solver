from flask import Flask, render_template, request, jsonify, session
from solver import solve_sudoku
import copy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # required for session tracking

# Example Sudoku puzzle (0 means empty cell)
PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


@app.route('/')
def index():
    session['attempts'] = 0
    return render_template('index.html', puzzle=PUZZLE)


@app.route('/submit', methods=['POST'])
def submit():
    """Handle submission attempts"""
    data = request.get_json()
    user_board = data['board']
    session['attempts'] += 1

    # Generate solved board
    solved_board = copy.deepcopy(PUZZLE)
    solve_sudoku(solved_board)

    if user_board == solved_board:
        return jsonify({'status': 'success', 'message': 'Puzzle solved successfully! 🎉'})
    elif session['attempts'] >= 3:
        return jsonify({'status': 'fail', 'message': 'Maximum attempts reached! 😢'})
    else:
        remaining = 3 - session['attempts']
        return jsonify({'status': 'retry', 'message': f'Incorrect solution. {remaining} attempts left.'})


@app.route('/solution', methods=['GET'])
def solution():
    solved = copy.deepcopy(PUZZLE)
    solve_sudoku(solved)
    return jsonify({'solution': solved})


@app.route('/restart', methods=['GET'])
def restart():
    session['attempts'] = 0
    return jsonify({'puzzle': PUZZLE, 'message': 'Puzzle restarted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
