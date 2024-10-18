#TicTacToe AI 

# By Brandon Christian

# Description: This project aims to use the Minimax algorithm to make optimal decisions in a game of tic tac toe against a human player ("O")
# It will recursivly explore all possible options when making decisions going through all possible moves to maximize its chances of winning the game
# While minimizing its own chances of lossing. As this project is being updated I will be working to implement Alpha-Beta pruning to optimize the 
# algorithm and reduce the number of nodes (game states) it needs to evaluate before making a move. 
# 

import tkinter as tk
import random
import sys

# Tic-tac-toe game board (3x3 grid)
GameBoard = [[' ' for _ in range(3)] for _ in range(3)]

# Difficulty level (easy, medium, hard)
difficulty = "hard"

# Reset the game board for a new game
def ResetGameBoard():
    for i in range(3):
        for j in range(3):
            GameBoard[i][j] = ' '

# Check if the game board is full
def GameBoardFull():
    for row in GameBoard:
        if ' ' in row:
            return False
    return True

# Check if a player has won the game
def CheckWinner(player):
    for i in range(3):
        # Rows and columns
        if GameBoard[i][0] == GameBoard[i][1] == GameBoard[i][2] == player:
            return True
        if GameBoard[0][i] == GameBoard[1][i] == GameBoard[2][i] == player:
            return True
    # Diagonals
    if GameBoard[0][0] == GameBoard[1][1] == GameBoard[2][2] == player:
        return True
    if GameBoard[0][2] == GameBoard[1][1] == GameBoard[2][0] == player:
        return True
    return False

# Evaluate the game board and return a score
def Evaluate(GameBoard):
    if CheckWinner('X'):
        return -1
    elif CheckWinner('O'):
        return 1
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def Minimax(GameBoard, depth, alpha, beta, maximizing, max_depth=None):
    score = Evaluate(GameBoard)

    # Base case: if someone has won or the board is full
    if score == 1:
        return score - depth
    elif score == -1:
        return score + depth
    elif GameBoardFull():
        return 0

    # Stop the recursion if we reach max_depth (for medium difficulty)
    if max_depth is not None and depth >= max_depth:
        return 0

    if maximizing:
        BestScore = -sys.maxsize
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'O'
                    score = Minimax(GameBoard, depth + 1, alpha, beta, False, max_depth)
                    GameBoard[i][j] = ' '
                    BestScore = max(score, BestScore)
                    alpha = max(alpha, BestScore)
                    if beta <= alpha:
                        break  # Beta cut-off
        return BestScore
    else:
        BestScore = sys.maxsize
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'X'
                    score = Minimax(GameBoard, depth + 1, alpha, beta, True, max_depth)
                    GameBoard[i][j] = ' '
                    BestScore = min(score, BestScore)
                    beta = min(beta, BestScore)
                    if beta <= alpha:
                        break  # Alpha cut-off
        return BestScore

# Make a move based on the difficulty level
def MakeMove():
    global difficulty
    if difficulty == "easy":
        # Make a random move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if GameBoard[i][j] == ' ']
        if empty_cells:
            move = random.choice(empty_cells)
            GameBoard[move[0]][move[1]] = 'O'
    elif difficulty == "medium":
        # Medium mode: limit depth of Minimax to 2
        BestScore = -sys.maxsize
        BestMove = None
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'O'
                    score = Minimax(GameBoard, 0, -sys.maxsize, sys.maxsize, False, max_depth=2)
                    GameBoard[i][j] = ' '
                    if score > BestScore:
                        BestScore = score
                        BestMove = (i, j)
        if BestMove:
            GameBoard[BestMove[0]][BestMove[1]] = 'O'
    else:
        # Hard mode: full Minimax with alpha-beta pruning
        BestScore = -sys.maxsize
        BestMove = None
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'O'
                    score = Minimax(GameBoard, 0, -sys.maxsize, sys.maxsize, False)
                    GameBoard[i][j] = ' '
                    if score > BestScore:
                        BestScore = score
                        BestMove = (i, j)
        if BestMove:
            GameBoard[BestMove[0]][BestMove[1]] = 'O'

# Update the GUI after each move
def update_gui():
    for i in range(3):
        for j in range(3):
            button_grid[i][j].config(text=GameBoard[i][j])

# Handle click events from the user
def on_click(row, col):
    if GameBoard[row][col] == ' ':
        GameBoard[row][col] = 'X'
        button_grid[row][col].config(text='X')
        if CheckWinner('X'):
            label.config(text="You win!")
        elif GameBoardFull():
            label.config(text="It's a draw!")
        else:
            MakeMove()
            update_gui()
            if CheckWinner('O'):
                label.config(text="Computer wins!")
            elif GameBoardFull():
                label.config(text="It's a draw!")

# Handle difficulty selection
def set_difficulty(selected_difficulty):
    global difficulty
    difficulty = selected_difficulty
    label.config(text=f"Difficulty set to: {difficulty.capitalize()}")

# Restart the game
def restart_game():
    ResetGameBoard()
    update_gui()
    label.config(text="Your turn!")

# Set up the GUI using Tkinter
root = tk.Tk()
root.title("Tic-Tac-Toe with AI")

# Create the Tic-Tac-Toe grid
button_grid = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        button = tk.Button(root, text='', font='normal 20', width=5, height=2,
                           command=lambda i=i, j=j: on_click(i, j))
        button.grid(row=i, column=j)
        button_grid[i][j] = button

# Create a label to show game status
label = tk.Label(root, text="Your turn!", font='normal 15')
label.grid(row=3, column=0, columnspan=3)

# Create buttons for difficulty selection
easy_button = tk.Button(root, text="Easy", command=lambda: set_difficulty("easy"))
easy_button.grid(row=4, column=0)

medium_button = tk.Button(root, text="Medium", command=lambda: set_difficulty("medium"))
medium_button.grid(row=4, column=1)

hard_button = tk.Button(root, text="Hard", command=lambda: set_difficulty("hard"))
hard_button.grid(row=4, column=2)

# Restart button to start a new game
restart_button = tk.Button(root, text="Restart", command=restart_game)
restart_button.grid(row=5, column=0, columnspan=3)

# Start the game loop
root.mainloop()
































































































