import random
import os

def initialize_board():
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board
def display_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    print("2048 Game".center(21, '-'))
    for row in board:
        print("|".join(f"{num}".center(5) if num != 0 else "     " for num in row))
        print("-" * 21)
def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_cells:
        return
    i, j = random.choice(empty_cells)
    board[i][j] = random.choice([2, 4])
def get_user_move():
    valid_moves = ['w', 'a', 's', 'd']
    move = input("Enter move (w/a/s/d): ").lower()
    while move not in valid_moves:
        move = input("Invalid input. Enter move (w/a/s/d): ").lower()
    return move
def transpose(board):
    return [list(row) for row in zip(*board)]
def reverse(board):
    return [row[::-1] for row in board]
def compress(board):
    new_board = []
    changed = False
    for row in board:
        new_row = [num for num in row if num != 0]
        new_row += [0] * (4 - len(new_row))
        if new_row != row:
            changed = True
        new_board.append(new_row)
    return new_board, changed
def merge(board):
    changed = False
    for row in board:
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                changed = True
    return board, changed
def move_board(board, direction):
    changed = False
    if direction == 'w':
        board = transpose(board)
        board, changed1 = compress(board)
        board, changed2 = merge(board)
        changed = changed1 or changed2
        board, _ = compress(board)
        board = transpose(board)
    elif direction == 's':
        board = transpose(board)
        board = reverse(board)
        board, changed1 = compress(board)
        board, changed2 = merge(board)
        changed = changed1 or changed2
        board, _ = compress(board)
        board = reverse(board)
        board = transpose(board)
    elif direction == 'a':
        board, changed1 = compress(board)
        board, changed2 = merge(board)
        changed = changed1 or changed2
        board, _ = compress(board)
    elif direction == 'd':
        board = reverse(board)
        board, changed1 = compress(board)
        board, changed2 = merge(board)
        changed = changed1 or changed2
        board, _ = compress(board)
        board = reverse(board)
    return board, changed
def is_game_over(board):
    for row in board:
        if 0 in row:
            return False
    # To Check horizontal merges 
    for row in board:
        for i in range(3):
            if row[i] == row[i + 1]:
                return False
    # To Check vertical merges
    transposed = transpose(board)
    for row in transposed:
        for i in range(3):
            if row[i] == row[i + 1]:
                return False
    return True
def has_won(board):
    for row in board:
        if 2048 in row:
            return True
    return False
def main():
    board = initialize_board()
    while True:
        display_board(board)
        if has_won(board):
            print("Congratulations! You've reached 2048!")
            break
        if is_game_over(board):
            print("Game Over! No more moves available.")
            break
        move = get_user_move()
        board, changed = move_board(board, move)
        if changed:
            add_new_tile(board)
        else:
            print("Move not possible. Try a different direction.")
if __name__ == "__main__":
    main()
