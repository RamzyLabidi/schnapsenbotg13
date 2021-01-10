"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

"""While programming bot we assumed that we were player 1"""
# Import the API objects
from api import State, Deck
import random


class Bot:
    #tessst
    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        #test
        # returns possible marriages for our plauer
        possible_marriages = Deck.get_possible_mariages(1)
        # gets the trump suit
        trump_suit = Deck.get_trump_suit()
        #look at moves in the state
        # Access cards in player hands
        played_cards = []
        opponents_played_card = State.get_opponents_played_card()
        moves = state.moves()
        chosen_move = moves[0]

        moves_trump_suit = []

        # Get all trump suit moves available
        for index, move in enumerate(moves):
            played_cards.append(move)
            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                moves_trump_suit.append(move)

        if len(moves_trump_suit) > 0:
            chosen_move = moves_trump_suit[0]
            return chosen_move

        # If the opponent has played a card
        if state.get_opponents_played_card() is not None:

            moves_same_suit = []

            # Get all moves of the same suit as the opponent's played card
            for index, move in enumerate(moves):
                # If the opponent's card is a non trump card:

                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)
                    for move in moves_same_suit:
                        if move % 5 == 1:
                            chosen_move = move
                        elif move % 5 == 0:
                            chosen_move = move
                        elif len(possible_marriages) == 0:
                            if move % 5 == 2:
                                chosen_move = move
                            elif move % 5 == 3:
                                chosen_move = move
                            elif move % 5 == 4:
                                chosen_move = move

                    if opponents_played_card % 5 == 1 or opponents_played_card % 5 == 0:
                        # does this take the opponents played card in account?
                        if len(moves_trump_suit) != 0:
                            for move in moves_trump_suit:
                                if move % 5 == 4:
                                    chosen_move = move
                                elif move % 5 == 3:
                                    chosen_move = move
                                elif move % 5 == 2:
                                    chosen_move = move
                                elif move % 5 == 1:
                                    chosen_move = move
                                elif move % 5 == 0:
                                    chosen_move = move
                        elif not self.protective_cards(moves, played_cards):
                            for move in moves:
                                if move % 5 == 4:
                                    chosen_move = move
                                elif move % 5 == 3:
                                    chosen_move = move
                                elif move % 5 == 2:
                                    chosen_move = move
                        elif self.protective_cards(moves, played_cards):
                            for move in moves:
                                if move % 5 == 4:
                                    chosen_move = move
                                elif move % 5 == 3:
                                    chosen_move = move
                                elif move % 5 == 2:
                                    chosen_move = move
                        else:
                            return random.choice(moves)
        # if we played a card, get played cards

        # Return a random choice
        return chosen_move

    def get_10(self, moves):
        for move in moves:
            if move % 5 == 1:
                return Deck.get_suit(move)

    def cards_in_suit_of_10(self, moves):
        count = 0
        for card in moves:
            if Deck.get_suit(card) == self.get_10(moves):
                count += 1
                return count

    def protective_cards(self, moves, played_cards):
        for card in played_cards:
            if card % 5 == 0 and Deck.get_suit(card) == self.get_10(played_cards):
                return False
        for card in moves:
            if card % 5 == 0 and Deck.get_suit(card) == self.get_10(moves):
                return False
            elif self.cards_in_suit_of_10(moves) > 2:
                return False
            elif Deck.get_suit(card) == self.get_10(moves):
                return True
