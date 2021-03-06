"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

infinity = float('inf')


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score_basic(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    score = len(own_moves)
    return float(score)

def custom_score_improved(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function returns the difference 
    between the number of moves available for self and the opponent player. 
    A mixing factor is used to compute weighted sum of the two instead of 
    plain addition.  

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    mixing_factor = 0.4
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(mixing_factor * own_moves + (1 - mixing_factor) * (-opp_moves))

def custom_score_opponent_moves(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function only returns the number of 
    moves available for opponent player.  

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = 0 # len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def custom_score_own_moves(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function only returns the number of 
    moves available for the player.  

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    return float(own_moves)

def custom_score_center_deviation(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function discourages the player to go to
    the boundaries of the board by discounting the distance to centre of the 
    board from the returned score. 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    mixing_factor = 0.8
    board_center = (game.width / 2.0, game.height / 2.0)
    current_location = game.get_player_location(player)
    distance_to_center = (current_location[0] - board_center[0]) ** 2 + (current_location[1] - board_center[1]) ** 2
    distance_to_center_normilized = distance_to_center / ( (board_center[0]) ** 2 + (board_center[1]) ** 2 )
    #print("distance to center = " + str(-distance_to_center))
    
    nrof_own_moves = len(game.get_legal_moves(player))
    nrof_own_moves_normilized = nrof_own_moves / 8.0 
    
    score = mixing_factor * nrof_own_moves_normilized + (1 - mixing_factor) * (- distance_to_center_normilized)
    #print('score = ' + str(score)) 
    
    return float(score)

def custom_score_lookahead_opponent(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function looks at the number of available
    moves for its own player subtracted by the average number of moves available
    for the opponent in the next round.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    if len(own_moves) == 0: 
        return float("-inf")
    
    opp_moves = 0.0
    for move in own_moves: 
        new_game = game.forecast_move(move)
        opp_moves += len(new_game.get_legal_moves(game.get_opponent(player)))
    # get the average moves that the opponent have 
    avg_opp_moves = opp_moves / len(own_moves)
    return float(len(own_moves) - avg_opp_moves)

def custom_score_lookahead_own(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function looks ahead one level deeper and
    returns the number of legal moves at the current step and the average of
    number of moves available due to each of the moves in previous step.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    if len(own_moves) == 0: 
        return float("-inf")
    mixing_factor = 0.4
    lookahead_moves = 0.0
    for move in own_moves: 
        lookahead_game = game.forecast_move(move)
        lookahead_moves += len(lookahead_game.get_legal_moves(player))
    lookahead_moves /= len(own_moves)   
    if lookahead_moves == 0: 
        # loosing game in the future
        return float("-inf") 
    
    score = mixing_factor * len(own_moves) + (1 - mixing_factor) * lookahead_moves
    return float(score)

def custom_score_lookahead_both(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This score function looks ahead one level deeper and
    returns the number of legal moves at the current step and the average of
    number of moves available due to each of the moves in previous step. 
    This look ahead is performed for both players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    mixing_factor = 0.5
    if len(own_moves) == 0: 
        return float("-inf")
    lookahead_moves = 0.0
    opp_moves_next_level = 0.0
    for move in own_moves: 
        lookahead_game = game.forecast_move(move)
        lookahead_moves += len(lookahead_game.get_legal_moves(player))
        # opponent moves
        opp_moves_next_level += len(lookahead_game.get_legal_moves(game.get_opponent(player)))
    lookahead_moves /= len(own_moves)   
    # get the average moves that the opponent have 
    opp_moves_next_level /= len(own_moves)

    if lookahead_moves == 0: 
        # loosing game in the future
        #return float("-inf")
        pass  
        
    score =  mixing_factor * (len(own_moves) - opp_moves) + (1 - mixing_factor) * (lookahead_moves - opp_moves_next_level)
    return float(score)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    #return custom_score_basic(game, player)
    #return custom_score_improved(game, player)
    #return custom_score_opponent_moves(game, player)
    #return custom_score_own_moves(game, player)
    #return custom_score_lookahead_opponent(game, player)
    #return custom_score_center_deviation(game, player)
    #return custom_score_lookahead_own(game, player)
    return custom_score_lookahead_both(game, player)



class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if len(legal_moves) == 0: 
            return (-1, -1)

        # initialize next move 
        move = legal_moves[0]
        TERMINAL_MOVE = [(-1, -1)]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method == 'minimax':
                search_alg = self.minimax
            elif self.method == 'alphabeta': 
                search_alg = self.alphabeta
            else: 
                raise Exception
            if self.iterative: 
                # if iterative deepening is activated, it starts from depth zero
                # and work it's way toward deeper levels of the decision tree
                depth = 0
            else: 
                # if iterative deepening is not activated, it only does the 
                # search once for the maximum depth of the tree
                depth = self.search_depth
            while self.iterative or depth <= self.search_depth and move not in TERMINAL_MOVE: 
                # go one level deeper in the search tree
                _, move = search_alg(game, depth)  
                depth += 1 

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass
        # Return the best move from the last completed search iteration
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        player = game.active_player
        
        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # depth zero means we are at the leaf
            next_move = (-1, -1)
            if depth == 0 or len(game.get_legal_moves()) == 0: 
                return self.score(game, player), next_move
            score = infinity
            for move in game.get_legal_moves(): 
                v, _ = max_value(game.forecast_move(move), depth - 1)
                # find the min(score, v) and the corresponding move
                if score > v: 
                    score = v 
                    next_move = move
            return score, next_move

        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # depth zero means we are at the leaf
            next_move = (-1, -1)
            if depth == 0 or len(game.get_legal_moves()) == 0: 
                return self.score(game, player), next_move
            score = -infinity
            for move in game.get_legal_moves(): 
                v, _ = min_value(game.forecast_move(move), depth - 1)
                # find the max(score, v) and the corresponding move
                if score < v: 
                    score = v 
                    next_move = move
            return score, next_move
            
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        # Do a search with a bounded depth 
        if maximizing_player:
            score, next_move = max_value(game, depth) 
        else: 
            raise NotImplemented

        return score, next_move   

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        
        def min_value(game, depth, alpha = -infinity, beta = infinity):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # initialize the next move
            next_move = (-1, -1)
            # depth zero means we are at the leaf
            if depth == 0 or len(game.get_legal_moves()) == 0: 
                return self.score(game, player), next_move
            score = infinity
            for move in game.get_legal_moves(): 
                v, _  = max_value(game.forecast_move(move), depth - 1, alpha, beta)
                # compare and find hte maximium score and the corresponding move
                if score > v: 
                    score = v 
                    next_move = move
                # pruning                  
                if score <= alpha: 
                    break
                # update the value for alpha
                beta = min(beta, score) 
            return score, next_move 

        def max_value(game, depth, alpha = -infinity, beta = infinity):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # initialize the next move
            next_move = (-1, -1)
            # depth zero means we are at the leaf
            if depth == 0 or len(game.get_legal_moves()) == 0: 
                return self.score(game, player), next_move
            score = -infinity
            for move in game.get_legal_moves(): 
                v, _  = min_value(game.forecast_move(move), depth - 1, alpha, beta)
                # compare and find hte maximium score and the corresponding move
                if score < v: 
                    score = v 
                    next_move = move
                # pruning                  
                if score >= beta: 
                    break
                # update the value for alpha
                alpha = max(alpha, score)
            return score, next_move
            
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        player = game.active_player

        if maximizing_player: 
            score, next_move = max_value(game, depth, alpha, beta)
        else: 
            raise NotImplemented

        return score, next_move   
