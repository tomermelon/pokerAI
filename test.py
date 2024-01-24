'''
import main
from Cards import Card
from Deck import Deck
from Player import Player

sidepot = 100

test1, test2, test3, test4, test5 = Player("John"), Player("Joe"), Player("Jeff"), Player("Joan"), Player("Jill")


river = [Card("Hearts", 10), Card("Hearts", 11), Card("Hearts", 12), Card("Hearts", 13), Card("Hearts", 14)]

players = [test1, test2, test3, test4, test5]
sidepotplayers = [test1, test2]
players[0].hand = [Card("Clubs", 2), Card("Diamonds", 3)]
players[1].hand = [Card("Diamonds", 2), Card("Clubs", 3)]
players[2].hand = [Card("Diamonds", 5), Card("Clubs", 4)]
players[3].hand = [Card("Diamonds", 6), Card("Clubs", 7)]
players[4].hand = [Card("Diamonds", 8), Card("Clubs", 9)]


main.winner(river,players, sidepot, sidepotplayers)
for i in players:
    print(i.totalamount())
'''

word = "raise 15"
word = word.split(" ")
digit = int(word[1])
print(digit)


