import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    The player who has fewer or equal marks is the next player.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # Player X goes if X has fewer or equal marks
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    An action is a tuple (i, j) where board[i][j] is EMPTY.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Assumes that the action is valid (i.e., (i, j) is an empty cell).
    """
    i, j = action
    new_board = [row[:] for row in board]  # Create a copy of the board
    new_board[i][j] = player(board)  # Set the current player's mark
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one (X or O), or None if there is no winner yet.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None  # No winner


def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    A game is over if there's a winner or if all cells are filled.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0  # No winner


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Uses the minimax algorithm to recursively evaluate the best move.
    """
    if terminal(board):
        return None  # No moves if the game is over

    current_player = player(board)
    if current_player == X:
        best_value = -math.inf
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            move_value = minimax_value(new_board)
            if move_value > best_value:
                best_value = move_value
                best_move = action
        return best_move
    else:
        best_value = math.inf
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            move_value = minimax_value(new_board)
            if move_value < best_value:
                best_value = move_value
                best_move = action
        return best_move


def minimax_value(board):
    """
    Recursively computes the minimax value for a given board state.
    The function evaluates the best score by exploring all possible game states.
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            new_board = result(board, action)
            best_value = max(best_value, minimax_value(new_board))
        return best_value
    else:
        best_value = math.inf
        for action in actions(board):
            new_board = result(board, action)
            best_value = min(best_value, minimax_value(new_board))
        return best_value
