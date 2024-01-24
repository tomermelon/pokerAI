import random
from Cards import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.fill()

    def fill(self):
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            for value in range(2, 15): #2=< x <15
                self.cards.append(Card(suit, value))

    def show(self):
        for card in self.cards:
            print(card.show())

    def shuffle(self ,stimes):
        random.seed()
        for i in range(stimes):
            half1 = []
            half2 = []
            length = len(self.cards)
            for card in range(length):
                if card < length/2:
                    half1.append(self.cards[card])
                else:
                    half2.append(self.cards[card])
            self.cards.clear()
            for card in range(length):
                pick = random.randint(1, 2)
                print(pick)
                if len(half1) == 0:
                    pick = 2

                elif len(half2) == 0:
                    pick = 1

                if pick == 1 and len(half1) > 0:
                    self.cards.append(half1.pop())

                elif pick == 2 and len(half2) > 0:
                    self.cards.append(half2.pop())

    def drawCard(self):
        return self.cards.pop()
