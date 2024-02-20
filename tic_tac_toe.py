
import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * (len(board) * 4 - 1))

def check_winner(board, player):
    size = len(board)
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(size):
        if all(board[row][col] == player for row in range(size)):
            return True
    if all(board[i][i] == player for i in range(size)) or \
       all(board[i][size - i - 1] == player for i in range(size)):
        return True
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == ' ']

def get_player_move(board):
    while True:
        try:
            move = int(input("please enter a Number "))
            if 1 <= move <= len(board) ** 2 and board[(move - 1) // len(board)][(move - 1) % len(board)] == ' ':
                return (move - 1) // len(board), (move - 1) % len(board)
            else:
                print("The selected location is not valid. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def make_computer_move(board, level):
    empty_cells = get_empty_cells(board)
    if level == 'easy':
        return random.choice(empty_cells)
    elif level == 'medium':
        return minimax(board, 'O', 2)[0]
    else:
        return minimax(board, 'O', 4)[0]

def minimax(board, player, depth):
    if player == 'O':
        best = (-1, -1, float("inf"))
    else:
        best = (-1, -1, -float("inf"))

    if depth == 0 or check_winner(board, 'O') or check_winner(board, 'X') or is_board_full(board):
        score = evaluate_board(board)
        return (-1, -1, score)

    for i, j in get_empty_cells(board):
        board[i][j] = player
        if player == 'O':
            score = minimax(board, 'X', depth - 1)[2]
        else:
            score = minimax(board, 'O', depth - 1)[2]
        board[i][j] = ' '

        if player == 'O':
            if score < best[2]:
                best = (i, j, score)
        else:
            if score > best[2]:
                best = (i, j, score)

    return best

def evaluate_board(board):
    size = len(board)
    score = 0
    for row in board:
        score += row.count('X') ** 2 - row.count('O') ** 2
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        score += column.count('X') ** 2 - column.count('O') ** 2
    diagonal1 = [board[i][i] for i in range(size)]
    diagonal2 = [board[i][size - i - 1] for i in range(size)]
    score += diagonal1.count('X') ** 2 - diagonal1.count('O') ** 2
    score += diagonal2.count('X') ** 2 - diagonal2.count('O') ** 2
    return score

def save_game(board):
    with open("game.txt", "w") as file:
        for row in board:
            file.write(" | ".join(row) + "\n")
            file.write("-" * (len(board) * 4 - 1) + "\n")

def load_game():
    try:
        with open("game.txt", "r") as file:
            lines = file.readlines()
            size = len(lines[0].strip().split(" | "))
            board = [[' ' for _ in range(size)] for _ in range(size)]
            for i, line in enumerate(lines):
                if i % 2 == 0:
                    row_values = line.strip().split(" | ")
                    for j in range(size):
                        board[i // 2][j] = row_values[j]
            return board
    except FileNotFoundError:
        return None

def main():
    print("Tic-Tac-Toe game - you (X) against the robot (O)!")
    while True:
        try:
            size = int(input("Please enter the size of the playing field (eg 3 for a 3x3 field):"))
            if size < 3:
                print("The size of the playing field must be at least 3.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        level = input("Please select the game level (easy/medium/hard):").lower()
        if level in ['easy', 'medium', 'hard']:
            break
        else:
            print("Invalid game level. Try again.")

    load_option = input("Do you want to play the previous game from the file? (Yes/No): ").lower()
    if load_option == "Yes":
        loaded_board = load_game()
        if loaded_board is not None:
            board = loaded_board
            print("The previous game was played from the game file.")
            print_board(board)
        else:
            print("The game file is not available. A new game starts.")
            board = [[' ' for _ in range(size)] for _ in range(size)]
            print_board(board)
    else:
        board = [[' ' for _ in range(size)] for _ in range(size)]
        print_board(board)

    human_player = 'X'
    computer_player = 'O'
    
    while True:
        # نوبت بازیکن انسان (X)
        if not is_board_full(board):
            print("Your turn (X):")
            row, col = get_player_move(board)
            board[row][col] = human_player
            print_board(board)

            if check_winner(board, human_player):
                print("you win! Congratulations.")
                save_game(board)
                break

        if is_board_full(board):
            print("The game ended in a draw.")
            save_game(board)
            break

        # نوبت ربات (O)
        if not is_board_full(board):
            print("Robot turn (O):")
            row, col = make_computer_move(board, level)
            board[row][col] = computer_player
            print("Robot (O) was placed in row {} and column {}.".format(row, col))
            print_board(board)

            if check_winner(board, computer_player):
                print("The robot won! Hopefully next time.")
                save_game(board)
                break

        if is_board_full(board):
            print("The game ended in a draw.")
            save_game(board)
            break

if __name__ == "__main__":
    main()
