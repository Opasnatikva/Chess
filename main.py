from flask import Flask, render_template, request, redirect, make_response, url_for
import json
import chessboard

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    """If the GET method is used, renders the homepage. If the POST method is used, creates a new game object,
        saves the initial board state, the game mode, and the active player as cookies, then proceeds to render
        the /game page"""
    if request.method == 'POST':
        init_game = chessboard.ChessBoard()
        response = make_response(redirect(url_for('game', game=init_game)))
        response.set_cookie(f'game_mode = {request.form["mode"]};')
        response.set_cookie(f'board_state = {json.dumps(init_game.board)};')
        response.set_cookie(f'active_player = {init_game.active_player};')
        return response
    return render_template('index.html')

@app.route('/game')
def game():
    game = chessboard.ChessBoard()
    game.board = json.loads(request.cookies.get('board_state'))  # Read board state from cookie
    game.active_player = request.cookies.get('active_player')  # Read active player from cookie
    if game.win_con(local_board=game.board):
        print(game.active_player)
        return render_template(url_for('victory'))
    if game.board_full(board=game.board):
        return render_template(url_for('draw'))
    print("continue")
    return render_template('game.html', game=game)
