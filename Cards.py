class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        if self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        elif self.value == 14:
            val = "Ace"
        else:
            val = self.value
        return "{} of {}".format(val, self.suit)



