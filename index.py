import random

def display_board(board):
    """Displays the Tic Tac Toe board."""
    n = len(board)
    row_labels = 'ABCDE'[:n]  # Adjust row labels based on board size
    print("  ", end="")
    for i in range(n):
        print(f"{i+1} ", end="")
    print()

    for i in range(n):
        print(f"{row_labels[i]} ", end="")
        for j in range(n):
            print(f"{board[i][j]} ", end="")
        print()

def player_input():
    """Gets player input for X or O marker."""
    marker = ''
    while not (marker == 'X' or marker == 'O'):
        marker = input("Player 1, do you want to be X or O? ").upper()

    return ('X', 'O') if marker == 'X' else ('O', 'X')

def place_marker(board, marker, position):
    """Places the marker on the board."""
    row = ord(position[0].upper()) - ord('A')
    col = int(position[1]) - 1
    board[row][col] = marker

def win_check(board, mark):
    """Checks if a player has won."""
    n = len(board)
    # Check rows
    for row in board:
        if all(cell == mark for cell in row):
            return True

    # Check columns
    for j in range(n):
        if all(board[i][j] == mark for i in range(n)):
            return True

    # Check diagonals
    if all(board[i][i] == mark for i in range(n)):
        return True
    if all(board[i][n - 1 - i] == mark for i in range(n)):
        return True

    return False

def choose_first():
    """Randomly chooses who goes first."""
    return 'Computer' if random.randint(0, 1) == 0 else 'Player'

def space_check(board, position):
    """Checks if a space on the board is empty."""
    row = ord(position[0].upper()) - ord('A')
    col = int(position[1]) - 1
    return board[row][col] == ' '

def player_choice(board):
    """Gets the player's next position."""
    n = len(board)
    while True:
        position = input(f"Choose a position (e.g., A1-{chr(ord('A') + n - 1)}{n}): ").upper()
        if len(position) == 2 and 'A' <= position[0] <= chr(ord('A') + n - 1) and '1' <= position[1] <= str(n):
            if space_check(board, position):
                return position
            else:
                print("That space is already occupied. Try again.")
        else:
            print(f"Invalid input. Please use the format A1-{chr(ord('A') + n - 1)}{n}.")


def computer_choice(board, computer_marker, player_marker):
    """Gets the computer's next position (basic AI)."""
    n = len(board)

    # Check for winning move
    for row_char in 'ABCDE'[:n]:
        for col_num in map(str, range(1, n + 1)):
            pos = row_char + col_num
            if space_check(board, pos):
                place_marker(board, computer_marker, pos)
                if win_check(board, computer_marker):
                    return pos
                else:
                    board[ord(row_char) - ord('A')][int(col_num) - 1] = ' '  # Undo move

    # Check for player winning move to block
    for row_char in 'ABCDE'[:n]:
        for col_num in map(str, range(1, n + 1)):
            pos = row_char + col_num
            if space_check(board, pos):
                place_marker(board, player_marker, pos)
                if win_check(board, player_marker):
                    board[ord(row_char) - ord('A')][int(col_num) - 1] = ' '  # Undo move
                    return pos
                else:
                    board[ord(row_char) - ord('A')][int(col_num) - 1] = ' '  # Undo move

    # Choose a random available spot
    available_positions = []
    for row_char in 'ABCDE'[:n]:
        for col_num in map(str, range(1, n + 1)):
            pos = row_char + col_num
            if space_check(board, pos):
                available_positions.append(pos)

    return random.choice(available_positions) if available_positions else None

def replay():
    """Asks if the player wants to play again."""
    return input("Do you want to play again? Enter Yes or No: ").lower().startswith('y')

def get_board_size():
    """Gets the desired board size from the player."""
    while True:
        try:
            size = int(input("Enter the desired board size (3, 4, or 5): "))
            if size in (3, 4, 5):
                return size
            else:
                print("Invalid board size. Please enter 3, 4, or 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

print('Welcome to Tic Tac Toe!')

while True:
    board_size = get_board_size()
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    player_marker, computer_marker = player_input()
    turn = choose_first()
    print(turn + ' will go first.')
    game_on = True

    while game_on:
        # ... (rest of the game logic remains the same, using the 'board' and 'board_size')
        if turn == 'Player':
            display_board(board)
            position = player_choice(board)
            place_marker(board, player_marker, position)

            if win_check(board, player_marker):
                display_board(board)
                print('Congratulations! You have won the game!')
                game_on = False
            else:
                if all(all(cell != ' ' for cell in row) for row in board):
                    display_board(board)
                    print('The game is a draw!')
                    game_on = False
                else:
                    turn = 'Computer'

        else:
            position = computer_choice(board, computer_marker, player_marker)
            if position:
                place_marker(board, computer_marker, position)

                if win_check(board, computer_marker):
                    display_board(board)
                    print('The computer has won!')
                    game_on = False
                else:
                    turn = 'Player'

    if not replay():
        break
