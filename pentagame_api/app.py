'''
Khizar Qureshi & Ntense Obono
app.py
Sep 18 2023
CS 347 - Advance Software Design 
'''

import flask
import json 
import sys
import argparse

app = flask.Flask(__name__)
games = {}
current = 0

'''Returns a string representation of the current board'''
def getBoard(board):
    formatted_board = ""
    for row in board:
        for spot in row:
            formatted_board += spot 
    return formatted_board    

def isCapturable(board, row, col): 
    char = board[row][col]
    if col < 19 and board[row][col+1] == char:
        return True
    elif row < 19 and board[row+1][col] == char:
        return True
    elif row < 19 and col < 19 and board[row+1][col+1] == char:
        return True
    elif col > 0 and board[row][col-1] == char:
        return True
    elif row > 0 and board[row-1][col] == char:
        return True
    elif row >0 and col > 0 and board[row-1][col-1] == char:
        return True
    return False
    
def updateX(board,row,col):
    nums = 0
    if isCapturable(board,row,col): 
        if col < 18 and col > 1 and board[row][col+2] and board[row][col-2] == "O":
            nums+=1
        elif row < 18 and row > 1 and board[row+2][col] and board[row-2][col]== "O":
            nums+=1
        elif row < 18 and col < 18 and row > 1 and col > 1 and board[row+2][col+2] and board[row-2][col-2]== "O":
            nums+=1
    return nums
        
def updateO(board,row,col):
    nums = 0
    if isCapturable(board,row,col): 
        if col < 18 and col > 1 and board[row][col+2] and board[row][col-2] == "X":
            nums+=1
        elif row < 18 and row > 1 and board[row+2][col] and board[row-2][col] == "X":
            nums+=1
        elif row < 18 and col < 18 and row > 1 and col > 1 and board[row+2][col+2] and board[row-2][col-2] == "X":
            nums+=1
    return nums
        

        

@app.route('/')
def hello():
    return 'Welcome to a simple API Flask implementation of Pente'


@app.route('/newgame/<player>')
def new_game(player):
    global current 
    current += 1
    gameID = current
    #boardSetup = "-" * 361
    boardSetup = [['-' for i in range(19)] for j in range(19)]
    if player == 'X' or player == 'x':
        boardSetup[19//2][19//2] = 'X'
    formatted_board = getBoard(boardSetup)
    gameState = 'player:' + player + '#' + 'board:' + formatted_board + '#' + 'capturedX: 0' + '#' + 'capturedO: 0'
    games[gameID] =  {'player': player, 'board': boardSetup, 'capturedX': 0, 'capturedO': 0}
    return json.dumps({'ID':gameID, 'state':gameState})



@app.route('/nextmove/<int:gameID>/<int:row>/<int:col>')
def new_move(gameID, row, col):
    #get states 
    gameState = games[gameID]
    player = gameState.get('player')
    board = gameState.get('board')
    capturedX = gameState.get('capturedX')
    capturedO = gameState.get('capturedO')
    
    #place opponent's spot
    if board[row][col] != '-':
        raise Exception("This spot is already taken!")   
    elif player == 'X' or player == 'x':
        board[row][col] = 'O'  
        capturedO = capturedO + updateO(board, row, col) 
    else:
        board[row][col] = 'X' 
        capturedX = capturedX + updateX(board, row, col)

    # place player's spot 
    temp = False
    for rowIndex, row in enumerate(board):
        for colIndex, col in enumerate(row):
            if col == "-":
                board[rowIndex][colIndex] = player 
                myRow, myCol = rowIndex, colIndex
                temp = True
                break
        if temp: break
        

    
    #recalculate captureX and captureY based on player's spot
    capturedO = capturedO + updateO(board, myRow, myCol) 
    capturedX = capturedX + updateX(board, myRow, myCol)

    #get new string representation of board          
    formatted_board = getBoard(board)
    # create new game state
    new_game_state = 'player:' + player + '#' + 'board:' + formatted_board + '#' + 'capturedX:' + str(capturedX) + '#' + 'capturedO:' + str(capturedO)
    #update the dictionary for the game_id
    games[gameID] =  {'player': player, 'board': board, 'capturedX': capturedX, 'capturedO': capturedO}
    return json.dumps({'ID':gameID, 'row':myRow, 'column': myCol, 'gameState': new_game_state})

# def isCapturable(board, row, col): 
#     char = board[row][col]
#     if col < 19 and board[row][col+1] == char:
#         return True
#     elif row < 19 and board[row+1][col] == char:
#         return True
#     elif row < 19 and col < 19 and board[row+1][col+1] == char:
#         return True
#     elif col > 0 and board[row][col-1] == char:
#         return True
#     elif row > 0 and board[row-1][col] == char:
#         return True
#     elif row >0 and col > 0 and board[row-1][col-1] == char:
#         return True
#     return False
    
# def updateX(board,row,col):
#     nums = 0
#     if isCapturable(board,row,col): 
#         if col < 18 and col > 1 and board[row][col+2] and board[row][col-2] == "O":
#             nums+=1
#         elif row < 18 and row > 1 and board[row+2][col] and board[row-2][col]== "O":
#             nums+=1
#         elif row < 18 and col < 18 and row > 1 and col > 1 and board[row+2][col+2] and board[row-2][col-2]== "O":
#             nums+=1
#     return nums

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Simple Flask application")
    parser.add_argument('host', help = 'the host on which this application is running')
    parser.add_argument('port', type = int, help = 'the port in which this application is listening')
    arguments = parser.parse_args()
    app.run(host = arguments.host, port = arguments.port, debug= True)
    
    
    