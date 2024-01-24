import random

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.chip1 = 10
        self.chip5 = 4
        self.chip10 = 2
        self.ispairnum = 0
        self.isthreeofakindnum = 0
        self.rank = 0
        self.handhighcard = 0
        self.straighthighcard = 0
        self.hc = None
        self.allincheck = False
        self.hands = None
        self.pokerhand = []
        self.pairlist = []
        self.checkstraight = []
        self.fullhand = []



    def draw(self, deck):
        self.hand.append(deck.drawCard())

    def showHand(self):
        print(self.name + "'s Hand:")
        for card in self.hand:
            print(card.show())

    def getvalue(self, Card):
        return Card.value

    def get_key(self, val, hands):
        for key, value in hands.items():
            if val == value:
                return key

    def decode(self, river):
        temp = []
        tempnum = []
        spades = []
        clubs = []
        diamonds = []
        hearts = []

        self.hc = self.highcard()


        for Card in self.hand:
            temp.append(Card)
            tempnum.append(Card.value)
        for Card in river:
            temp.append(Card)
            tempnum.append(Card.value)
        tempnum.sort()
        self.fullhand = temp.copy()

        for Card in temp:
            if Card.suit == "Spades":
                spades.append(Card)
            elif Card.suit == "Clubs":
                clubs.append(Card)
            elif Card.suit == "Diamonds":
                diamonds.append(Card)
            elif Card.suit == "Hearts":
                hearts.append(Card)

        suitnum = [len(spades), len(clubs), len(diamonds), len(hearts)]

        temp.sort(key=self.getvalue)
        tempsuit= [spades, clubs, diamonds, hearts]
        self.hands = {"Pair": self.ispair(temp),
                 "Two Pair": self.istwopair(temp),
                 "Three of a Kind": self.isthreeofakind(temp),
                 "Straight": self.isstraight(tempnum),
                 "Flush": self.isflush(tempsuit),
                 "Full House": self.isfullhouse(temp),
                 "Four of a Kind": self.isfourofakind(temp),
                 "Straight Flush": self.isstraightflush(tempnum, tempsuit),
                 "Royal Flush": self.isroyalflush(tempnum, tempsuit, suitnum)}

        if len(river) > 4:
            self.setpokerhand(tempnum, suitnum)

#ispairnum doesnt work, make sure we have highest pair
    
    def ispair(self, temp):
        for i in temp:
            for j in temp:
                if j.value == i.value and j.suit != i.suit and j.value != self.isthreeofakindnum:
                    self.ispairnum = j.value
                    self.rank = max(self.rank, 1)
                    if self.rank == 1:
                        self.handhighcard = max(j.value, self.handhighcard)
        if self.ispairnum > 0:
            return True

        return False

    def istwopair(self, temp):
        count = 0
        storedcount = 0
        for i in temp:
            for j in temp:
                if j.value == i.value and j.suit != i.suit and j.value != storedcount:
                    storedcount = j.value
                    count += 1
                    self.pairlist.append(storedcount)
        if count >= 2:
            self.rank = max(self.rank, 2)
            if self.rank == 2:
                self.handhighcard = max(self.pairlist)
            return 1
        elif count >= 1:
            return .5
        else:
            return 0

    def isthreeofakind(self, temp):
        for i in temp:
            for j in temp:
                for y in temp:
                    if (j.value == i.value and j.value == y.value) and (j.suit != i.suit and j.suit != y.suit) and (y.suit != i.suit):
                        self.isthreeofakindnum = i.value
                        self.rank = max(self.rank, 3)
                        if self.rank == 3:
                            self.handhighcard = max(i.value, self.handhighcard)
                        return 1
        if self.ispair(temp):
            return .6
        return 0

    def isstraight(self, tempnum):
        maxstraight = 0
        count = 1
        storedcount = 0

        for i in range(len(tempnum)-1):
            if tempnum[i] == tempnum[i+1]-1:
                count += 1
                self.checkstraight.append(i)
                if count >= 4:
                    maxstraight = tempnum[i+1]
            elif tempnum[i] == tempnum[i+1]:
                pass
            else:
                if count > storedcount:
                    storedcount = count
                count = 1

        if storedcount >= 4:
            self.rank = max(self.rank, 4)
            if self.rank == 4:
                self.handhighcard = maxstraight
            self.straighthighcard = maxstraight
            return 1
        elif storedcount != 0:
            return storedcount/4
        return 0

    def isflush(self,tempsuit):
        storedlength = 0
        high = 0
        for suit in tempsuit:
            if len(suit) >=5:
                self.rank = max(self.rank, 5)
                for s in suit:
                    if s.value > high:
                        high = s.value
                if self.rank == 5:
                    self.handhighcard = high
                return 1
            elif len(suit) > storedlength:
                storedlength = len(suit)
        if storedlength > 1:
            return storedlength/5
        return 0

    def isfullhouse(self,temp):
        if self.isthreeofakind(temp) == 1 and self.ispair(temp):
            if self.ispairnum != self.isthreeofakindnum and self.isthreeofakindnum != 0:
                self.rank = max(self.rank, 6)
                return True
        if self.isthreeofakind(temp) == 1:
            return .6
        elif self.istwopair(temp) == 1:
            return .8
        elif self.ispair(temp):
            return .4
        return False

    def isfourofakind(self,temp):
        storedvalue = 0
        fourkindnum = 0
        count = 0
        for i in temp:
            if storedvalue == 0:
                storedvalue = i.value
            if storedvalue == i.value:
                count +=1
                if count == 4:
                    fourkindnum = storedvalue
            else:
                storedvalue = i.value
                count = 1

        if fourkindnum > 0:
            self.rank = max(self.rank, 7)
            if self.rank == 7:
                self.handhighcard = fourkindnum
            return 1
        elif count > 1:
            return count/4
        return False

    def isstraightflush(self,tempnum, tempsuit):
        if self.isflush(tempsuit) == 1 and self.isstraight(tempnum) == 1:
            self.rank = max(self.rank, 8)
            if self.rank == 8:
                self.handhighcard = self.straighthighcard
            return 1
        elif self.isflush(tempsuit) or self.isstraight(tempnum):
            return .5
        return False

    def isroyalflush(self, tempnum, tempsuit, suitnum):
        highcards = [10, 11, 12, 13, 14]
        count = 0
        commonsuit = ""

        ind = max(suitnum)
        ind2 = suitnum.index(ind)
        if ind2 == 0:
            commonsuit = "Spades"
        if ind2 == 1:
            commonsuit = "Clubs"
        if ind2 == 2:
            commonsuit = "Diamonds"
        if ind2 == 3:
            commonsuit = "Hearts"
        if self.isstraightflush(tempnum, tempsuit):
            for i in tempsuit[ind2]:
                if i.value in highcards:
                    count +=1

        if count == 5:
            self.rank = max(self.rank, 9)
            return 1
        elif count > 1:
            return count/5
        return False

    def highcard(self):
        templist = []
        for i in self.hand:
            templist.append(i.value)
        return max(templist)



    def allin(self):
        temp = self.chip1 + self.chip5 * 5 + self.chip10 * 10
        self.chip1 = 0
        self.chip5 = 0
        self.chip10 = 0
        self.allincheck = True
        return temp

    def take(self, call):
        temp = call
        while call > 0:
            if call <= self.chip1 + self.chip5 *5 + self.chip10 * 10:
                if call >= 10 and self.chip10 != 0:
                    call -= 10
                    self.chip10 -= 1
                elif call >= 5 and self.chip5 != 0:
                    call -= 5
                    self.chip5 -= 1
                elif call >= 1 and self.chip1 != 0:
                    call -= 1
                    self.chip1 -= 1

                else:
                    if call < 5 and self.chip5 >= 1:
                        self.chip5 -= 1
                        self.chip1 += 5
                    else:
                        self.chip10 -= 1
                        self.chip5 += 2

            else:
                #(make all in method and fold method)
                print("You don't have enough money to call. Would you like to go all in(1), or fold(2)?")
                response = input()
                if response == "1" and self.totalamount() > 0:
                    temp = self.allin()
                    call = 0
                elif response == "2":
                    temp = -1
                    call = 0
                elif response == "1" and self.totalamount() ==  0:
                    print("You are bankrupt, you must fold.")
                    temp = -1
                    call = 0
                else:
                    print("Please enter a valid choice.")
        return temp

    def get(self, pot):
        temp = pot
        while pot > 0:
            if pot >= 10:
                pot -= 10
                self.chip10 += 1
            elif pot >= 5:
                pot -= 5
                self.chip5 += 1
            elif pot >= 1:
                pot -= 1
                self.chip1 += 1

    def displaychips(self):
        print(f"1 Chips: {self.chip1}")
        print(f"5 Chips: {self.chip5}")
        print(f"10 Chips: {self.chip10}")
        print(f"Total: {self.chip1 + self.chip5 * 5 + self.chip10 * 10}")

    def totalamount(self):
        return self.chip1 + self.chip5 * 5 + self.chip10 * 10

    def reset(self):
        self.hand.clear()
        self.ispairnum = 0
        self.isthreeofakindnum = 0
        self.rank = 0
        self.handhighcard = 0
        self.straighthighcard = 0
        self.hc = None
        self.allincheck = False

    def decidemove(self, pot, call, river, allincount):
        self.decode(river)

        if allincount >= 1:
            if self.rank >= 3 or random.randint(1,50) > 40:
                return "all in"
            else:
                return "fold"


        if call == 0 or len(river) == 0:
            return "call"
        if self.totalamount() == 0:
            return "fold"
        if call > self.totalamount() and self.rank >= 4:
            return "all in"
        elif call > self.totalamount():
            count = 1
            for i in self.hands.values():
                if count > 3:
                    if i >= .6 and len(river) <= 3:
                        return "all in"
                else:
                    count +=1

            return "fold"

        if len(river) == 4 and self.rank == 0:
            if self.hc >= 13:
                if random.randint(1, 100) > 50:
                    return "call"
                else:
                    return "fold"
            else:
                if random.randint(1, 100) > 95:
                    return "call"
                else:
                    return "fold"

        if len(river) == 1 and self.hands["Pair"] == 1:
            return f"raise {round(random.randint(1,50)/100 * self.totalamount())}"

        if self.rank >= 3:
            return f"raise {round(random.randint(30,90)/100 * self.totalamount())}"

        if self.rank >= 8:
            return "all in"

        if len(river) > 0:
            if random.randint(1,100) > 30:
                return "call"
            else:
                return f"raise {round(random.randint(1,30)/100 * self.totalamount())}"

    def setpokerhand(self, tempnum, suitnum):
        tempnumcopy = tempnum.copy()
        if self.rank == 0:
            for i in range(5):
                self.pokerhand.append(tempnumcopy.pop())
        elif self.rank == 1:
            self.pokerhand.append(self.ispairnum)
            self.pokerhand.append(self.ispairnum)
            tempnumcopy.remove(self.ispairnum)
            tempnumcopy.remove(self.ispairnum)
            for i in range(3):
                self.pokerhand.append(tempnumcopy.pop())

        elif self.rank == 2 or self.rank == 7:
            if self.rank == 2:
                for i in self.pairlist:
                    self.pokerhand.append(i)
                    tempnumcopy.remove(i)

            else:
                for i in range(4):
                    self.pokerhand.append(self.handhighcard)
                    tempnumcopy.remove(i)

            self.pokerhand.append(tempnumcopy[0])

        elif self.rank == 3:
            for i in range(3):
                self.pokerhand.append(self.isthreeofakindnum)
                tempnumcopy.remove(self.isthreeofakindnum)

            for i in range(2):
                self.pokerhand.append(tempnumcopy.pop())

        else:
            if self.rank == 4 or self.rank == 8:
                self.pokerhand = self.checkstraight.copy()

            elif self.rank == 5:
                for i in suitnum:
                    if i >= 5:
                        ind = suitnum.index(i)
                        suitcheck= ['spades', 'clubs', 'diamonds', 'hearts']
                        for j in self.fullhand:
                            if j.suit == suitcheck[ind]:
                                self.pokerhand.append(j.value)

            elif self.rank == 6:
                for i in range(3):
                    self.pokerhand.append(self.isthreeofakindnum)
                self.pokerhand.append(self.ispairnum)
                self.pokerhand.append(self.ispairnum)

                                


