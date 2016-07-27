"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Takes a board and computer player as input, then plays through
    a trial game which is then scored by mc_update_scores to
    help the computer player decide on its next move.
    """
    empty = board.get_empty_squares()
    curplayer = player
    winner = None

    while winner == None:
        move = random.choice(empty)
        board.move(move[0], move[1], curplayer)
        winner = board.check_win()
        curplayer = provided.switch_player(curplayer)
        empty = board.get_empty_squares()


def mc_update_scores(scores, board, player):
    """
    Takes in a list of scores that correlate to board positions and
    updates the scores for the computer player according to the
    result of the trial board being passed.
    """
    winner = board.check_win()
    current, other = get_scoring_squares(board, player)

    if winner == player:
        for dummy_cur in current:
            scores[dummy_cur[0]][dummy_cur[1]] += SCORE_CURRENT
        for dummy_oth in other:
            scores[dummy_oth[0]][dummy_oth[1]] -= SCORE_OTHER
    elif winner == provided.switch_player(player):
        for dummy_cur in current:
            scores[dummy_cur[0]][dummy_cur[1]] -= SCORE_CURRENT
        for dummy_oth in other:
            scores[dummy_oth[0]][dummy_oth[1]] += SCORE_OTHER


def get_scoring_squares(board, player):
    """
    This returns two lists of tuples representing the moves of
    both players in a trial game, which is then scored by
    mc_update_scores.
    """
    current = []
    other = []
    other_player = provided.switch_player(player)
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                current.append((row, col))
            elif board.square(row, col) == other_player:
                other.append((row, col))
    return current, other


def get_best_move(board, scores):
    """
    Creates a list of top scoring moves for the computer player and
    return a randomly selected one from that list.
    """
    poss_move_scores = []
    best_moves = []
    empty = board.get_empty_squares()
    for score in empty:
        poss_move_scores.append(scores[score[0]][score[1]])
    highest_score = max(poss_move_scores)
    for score in empty:
        if scores[score[0]][score[1]] == highest_score:
            best_moves.append((score[0],score[1]))
    return random.choice(best_moves)


def mc_move(board, player, trials):
    """
    Uses mc_trial and mc_update_scores to score possible moves, and
    and then return one of the best possible moves available.
    """
    trial = 0
    scores = [[0 for dummycol in range(board.get_dim())]
              for dummyrow in range(board.get_dim())]
    while trial < trials:
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        trial += 1
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
