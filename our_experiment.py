"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
import random
import matplotlib.pyplot as plt
from bots.rdeep import rdeep


def empty(n):
    """
    :param n: Size of the matrix to return
    :return: n by n matrix (2D array) filled with 0s
    """
    return [[0 for i in range(n)] for j in range(n)]


"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""


# Import the API objects


def is_10(moves):
    for i in range(len(moves)):
        if moves[0][0] % 5 == 1:
            return Deck.get_suit(i)


def cards_in_suit_of_10(moves):
    count = 0
    for i in range(len(moves)):
        if Deck.get_suit(i) == is_10(moves):
            count += 1
    return count


def protective_cards(moves, played_cards):
    for i in range(len(played_cards)):
        if played_cards[0][0] % 5 == 0 and Deck.get_suit(i) == is_10(played_cards):
            return False
    for i in range(len(moves)):
        if played_cards[0][0] % 5 == 0 and Deck.get_suit(i) == is_10(moves):
            return False
        elif cards_in_suit_of_10(moves) > 2:
            return False
        elif Deck.get_suit(i) == is_10(moves):
            return True


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type:#(State) -> tuple[int, int]

        # All legal moves
        moves = state.moves()
        chosen_move = moves[0]
        # ask TA
        # Deck.get_possible_mariages(state.whose_turn())
        moves_trump_suit = []
        played_cards = []  # Get all trump suit moves available
        for index, move in enumerate(moves):
            played_cards.append(move)
            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                moves_trump_suit.append(move)
                for move in moves_trump_suit:
                    if move[0] % 5 == 1:
                        chosen_move = move
                        return chosen_move
                    elif move[0] % 5 == 0:
                        chosen_move = move
                        return chosen_move
                    elif move[0] % 5 == 2:
                        chosen_move = move
                        return chosen_move
                    elif move[0] % 5 == 3:
                        chosen_move = move
                        return chosen_move
                    elif move[0] % 5 == 4:
                        chosen_move = move
                        return chosen_move
            if state.get_opponents_played_card() is not None and int(
                    state.get_opponents_played_card()) % 5 == 1 or state.get_opponents_played_card() is not None and int(
                state.get_opponents_played_card()) % 5 == 0:
                if len(moves_trump_suit) > 0:
                    for move in moves_trump_suit:
                        if move[0] % 5 == 4:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 3:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 2:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 1:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 0:
                            chosen_move = move
                            return chosen_move
                elif not protective_cards(moves, played_cards):
                    for move in moves:
                        if move[0] % 5 == 4:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 3:
                            chosen_move = move
                            return chosen_move
                        elif move[0] % 5 == 2:
                            chosen_move = move
                            return chosen_move
            else:
                return random.choice(moves)
        """
        if len(moves_trump_suit) > 0:
            chosen_move = moves_trump_suit[0]
            return chosen_move
        """
        if state.get_opponents_played_card() is None:
            non_trump_cards = moves

            if len(moves_trump_suit) > 0:
                i = 0
                for trump_card in moves_trump_suit:
                    if trump_card == moves[i]:
                        non_trump_cards.remove(trump_card)
                for card in non_trump_cards:
                    if card[0] % 5 == 4:
                        chosen_move = card
                        return chosen_move
                    elif card[0] % 5 == 3:
                        chosen_move = card
                        return chosen_move
                    elif card[0] % 5 == 2:
                        chosen_move = card
                        return chosen_move
                    elif card[0] % 5 == 1:
                        chosen_move = card
                        return chosen_move
                    elif card[0] % 5 == 0:
                        chosen_move = card
                        return chosen_move
            else:
                return random.choice(moves)

        # If the opponent has played a card
        if state.get_opponents_played_card() is not None:

            moves_same_suit = []

            # Get all moves of the same suit as the opponent's played card
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)

            if len(moves_same_suit) > 0:
                chosen_move = moves_same_suit[0]
                return chosen_move

        # Get move with highest rank available, of any suit
        for index, move in enumerate(moves):
            if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
                chosen_move = move

        return chosen_move


# For experiments, its good to have repeatability, so we set the seed of the random number generator to a known value.
# That way, if something interesting happens, we can always rerun the exact same experiment
seed = random.randint(1, 1000)
print('Using seed {}.'.format(seed))
random.seed(seed)

# Parameters of our experiment
STEPS = 40
REPEATS = 10

inc = 1.0 / STEPS

# Make empty matrices to count how many times each player won for a given
# combination of parameters
won_by_1 = empty(STEPS)
won_by_2 = empty(STEPS)

# We will move through the parameters from 0 to 1 in STEPS steps, and play REPEATS games for each
# combination. If at combination (i, j) player 1 winds a game, we increment won_by_1[i][j]

for i in range(STEPS):
    for j in range(STEPS):
        for r in range(REPEATS):

            # Make the players
            player1 = Bot()
            player2 = Bot()

            state = State.generate()

            # play the game
            while not state.finished():
                player = player1 if state.whose_turn() == 1 else player2
                state = state.next(player.get_move(state))

            # TODO Maybe add points for state.winner()
            if state.finished():
                winner, points = state.winner()
                if winner == 1:
                    won_by_1[i][j] += points


                else:
                    won_by_2[i][j] += points

        print('finished {} vs {}'.format(inc * i, inc * j))

# heights of bars
height = [len(won_by_1), len(won_by_2)]
left = [1, 2]
# labels for bars
tick_label = ['one', 'two']

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label,
        width=0.8, color=['red', 'green'])

# naming the x-axis
plt.xlabel('x - axis')
# naming the y-axis
plt.ylabel('y - axis')
# plot title
plt.title('My bar chart!')

# function to show the plot
plt.show()

plt.savefig('our_experiment.pdf')
