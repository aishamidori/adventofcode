from collections import defaultdict
from copy import copy, deepcopy

import sys

class Player:
    def __init__(self, player_num, initial_cards):
        self.player_num = player_num
        self.cards = initial_cards

    def play_card(self):
        card = None
        if self.cards:
            card = self.cards[0]

            if self.cards:
                self.cards = self.cards[1:]

        return card

    def receive_cards(self, new_cards):
        self.cards += new_cards

    def calculate_score(self):
        scale = 1
        score = 0
        print("Calculating score from cards", ", ".join(str(card) for card in self.cards))
        while self.cards:
            card = self.cards.pop()
            score += scale * card
            print("score +=", scale, "*", card)
            scale += 1
        return score

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
    round_num = 1
    while True:

        if not players[0].cards:
            print("Player 2 wins the game!")
            return players[1].calculate_score()
            break

        if not players[1].cards:
            print("Player 1 wins the game!")
            return players[0].calculate_score()
            break

        print("-- Round %d --" % round_num)
        print("Player 1's deck:", ", ".join(str(card) for card in players[0].cards))
        print("Player 2's deck:", ", ".join(str(card) for card in players[1].cards))

        player_1_card = players[0].play_card()
        player_2_card = players[1].play_card()
        print("Player 1 plays: %d" % player_1_card)
        print("Player 2 plays: %d" % player_2_card)


        cards = [player_1_card, player_2_card]
        cards.sort(reverse=True)
        if player_1_card > player_2_card:
            print("Player 1 wins the round!")
            players[0].receive_cards(cards)
        else:
            print("Player 2 wins the round!")
            players[1].receive_cards(cards)

        round_num += 1

def part2(processed):
    pass

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print(part1(processed))
        #print(part2(processed))
