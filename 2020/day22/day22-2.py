from collections import defaultdict
from copy import copy, deepcopy

import sys

previous_rounds_by_game = defaultdict(list)

class Player:
    def __init__(self, player_num, initial_cards):
        self.player_num = player_num
        self.cards = {
            1: initial_cards
        }

    def play_card(self, subgame=1):
        card = None
        if self.cards[subgame]:
            card = self.cards[subgame][0]
            if self.cards[subgame]:
                self.cards[subgame] = self.cards[subgame][1:]
        return card

    def receive_cards(self, new_cards, subgame=1):
        self.cards[subgame] += new_cards

    def calculate_score(self, subgame=1):
        scale = 1
        score = 0
        #print("Calculating score from cards", ", ".join(str(card) for card in self.cards[subgame]))
        card_copy = self.cards[subgame][:]
        while self.cards[subgame]:
            card = self.cards[subgame].pop()
            score += scale * card
            #print("score +=", scale, "*", card)
            scale += 1
        self.cards[subgame] = card_copy
        return score

    def start_subgame(self, num_cards_to_copy, from_game=1):
        max_subgame_num = max(self.cards.keys())
        new_subgame = max_subgame_num + 1
        self.cards[new_subgame] = self.cards[from_game][:num_cards_to_copy]
        #print("Started new subgame", new_subgame, "with cards", ", ".join(str(card) for card in self.cards[new_subgame]))
        return new_subgame

def preprocess(file_path):
    players = []
    with open(file_path) as f:
        file_contents = f.readlines()
        i = 0
        while i < len(file_contents):
            player = file_contents[i][7]
            i += 1

            next_line = file_contents[i]
            cards = []
            while next_line != '\n':
                cards.append(int(next_line))
                i += 1
                next_line = file_contents[i]

            i += 1
            players.append(Player(player, cards))
    return players

def part1(players):
    play_game(players, subgame=1)

def play_game(players, subgame=1):
    global previous_rounds_by_game
    round_num = 1
    while True:

        if not players[0].cards[subgame]:
            print("The winner of game %d is Player 2! (score = %d)" % (subgame, players[1].calculate_score(subgame=subgame)))
            return players[1]

        if not players[1].cards[subgame]:
            print("The winner of game %d is Player 1! (score = %d)" % (subgame, players[0].calculate_score(subgame=subgame)))
            return players[0]

        #print("-- Round %d (Game %d)--" % (round_num, subgame))
        #print("Player 1's deck:", ", ".join(str(card) for card in players[0].cards[subgame]))
        #print("Player 2's deck:", ", ".join(str(card) for card in players[1].cards[subgame]))

        # Check for matching previous rounds and add this round to previous rounds
        round_hands = (players[0].cards[subgame], players[1].cards[subgame])
        if round_hands in previous_rounds_by_game[subgame]:
            #print("Player 1 wins game %d because we saw this round before" % subgame)
            return players[0]
        previous_rounds_by_game[subgame].append(round_hands)

        player_1_card = players[0].play_card(subgame=subgame)
        player_2_card = players[1].play_card(subgame=subgame)
        #print("Player 1 plays: %d" % player_1_card)
        #print("Player 2 plays: %d" % player_2_card)


        # If players have at least as many cards remaining in their deck as the value of the card they just drew
        if len(players[0].cards[subgame]) >= player_1_card and len(players[1].cards[subgame]) >= player_2_card:
            # The winner of the round is determined in a recursive game
            #print("Playing a sub-game to determine the winner...")
            subgame_num = players[0].start_subgame(num_cards_to_copy=player_1_card, from_game=subgame)
            players[1].start_subgame(num_cards_to_copy=player_2_card, from_game=subgame)
            #print("=== Game %d ===" % subgame_num)
            winner = play_game(players, subgame=subgame_num)
            if winner == players[0]:
                players[0].receive_cards([player_1_card, player_2_card], subgame=subgame)
            else:
                players[1].receive_cards([player_2_card, player_1_card], subgame=subgame)
            #print("=== Back to Game %d ===" % subgame)

        # Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.
        else:
            if player_1_card > player_2_card:
                #print("Player 1 wins round %d of game %d!" % (round_num, subgame))
                players[0].receive_cards([player_1_card, player_2_card], subgame=subgame)
            else:
                #print("Player 2 wins round %d of game %d!" % (round_num, subgame))
                players[1].receive_cards([player_2_card, player_1_card], subgame=subgame)

        round_num += 1

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print(part1(processed))
        ##print(part2(processed))
