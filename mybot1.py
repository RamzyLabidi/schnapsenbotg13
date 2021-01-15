"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
import random


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
        #ask TA
        #Deck.get_possible_mariages(state.whose_turn())
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
