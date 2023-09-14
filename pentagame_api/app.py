import flask
import json 
import sys
import argparse

app = flask.Flask(__name__)
games = {}
current = 0

"----------------------------"


@app.route('/')
def hello():
    return 'Welcome to a simple API implementation of Penta'

@app.route('/newgame/<player>')
def new_game(player):
    global current 
    current += 1
    gameID = current
    boardSetup = [['-' for i in range(19)] for j in range(19)]
    if player == 'X' or player == 'x':
        boardSetup[19//2][19//2] = 'X'
    
    gameState = {'player': player, 'board': boardSetup, 'capturedX': 0, 'capturedO': 0}
    games[gameID] = gameState
    return json.dumps({'ID':gameID, 'state':gameState})

@app.route('/nextmove/<int:gameID>/<int:row>/<int:col>')
def new_move(gameID, row, col):
    gameState = games[gameID]
    player = gameState.get('player')
    board = gameState.get('board')
    if board[row][col] != '-':
        return 'X' #this isn't a valid move not sure about this part
    else:
        myRow, myCol = row, col 
        board[myRow][myCol] == player
    return json.dumps({'ID':gameID, 'row':myRow, 'column': myCol, 'gameState': gameState})

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Simple Flask application")
    parser.add_argument('host', help = 'the host on which this application is running')
    parser.add_argument('port', type = int, help = 'the port in which this application is listening')
    arguments = parser.parse_args()
    app.run(host = arguments.host, port = arguments.port, debug= True)