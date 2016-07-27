"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    winner = board.check_win()

    if winner:
        return (SCORES[winner], (-1, -1))
    else:
        poss_moves = board.get_empty_squares()

        mm_score = -2
        best_score = -2
        best_move = (-1, -1)

        for move in poss_moves:
            mm_board = board.clone()
            mm_board.move(move[0], move[1], player)

            next_player = provided.switch_player(player)
            next_mm = mm_move(mm_board, next_player)
            poss_score = next_mm[0]

            if poss_score * SCORES[player] > mm_score:
                mm_score = poss_score * SCORES[player]
                best_score = poss_score
                best_move = move
            if mm_score == 1:
                return (best_score, best_move)

    return best_score, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
