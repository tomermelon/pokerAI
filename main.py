"""
TODO:
make ai make choices (download from somewhere else)
river is giving the same value over and over (print out entire deck to check)
anti round raising and calling addition messed up
"""

from Deck import Deck
from Player import Player
import random
from Cards import Card

tempcall = 0
call = 1
pot = 0
sidepot = 0
tempallin = 0
lessallin = 0
allincount = 0
sidepotplayers = set()
allplayers = []
players = []
deck = None
river = []
folded = False



def fold(player):
    global players
    players.remove(player)

def bet(player):
    global call, pot, tempcall, tempallin, sidepot, lessallin, allincount, sidepotplayersv, folded #, players
    #current bet total, call count, player.chip1 -= 1(for anti, don't put into this function)
    #if temp = -1, it means player has folded, must be removed
    if sidepot > 0:
        print(f"Pot: {pot}\nCall: {call}\nSide Pot:{sidepot}")
    else:
        print(f"Pot: {pot}\nCall: {call}")
    player.displaychips()
    while True:
        print("Do you want to call, fold, raise, or go all in?")
        response = input().lower()
        if response == "call":
            amount = player.take(call)
            tempcall += 1
            if amount == -1:
                fold(player)
                folded = True
            else:
                pot += amount
            break
        elif response == "raise":
            while True:
                response = input("How much do you want to raise?")
                if response.isnumeric():
                    response = int(response)
                    if response + call <= player.totalamount():
                        call = response + call
                        pot += player.take(call)
                        print(f"Pot: {pot}\nCall: {call}")
                        tempcall = 1
                        break
                    elif response == 0:
                        break
                    else:
                        print("Please enter a number you can afford or enter \"0\" to cancel.")

                else:
                    print("Please enter a valid number.")
            if response != 0:
                break
        elif response == "fold":
            fold(player)
            folded = True
            tempcall += 1
            break
        elif response == "all in" and player.totalamount() > 0:
            tempcall += 1
            if tempallin == 0:
                pot += player.totalamount()
                call = player.totalamount()
                allincount += 1
                tempallin = player.totalamount()
            else:
                if player.totalamount() > tempallin:
                    allincount += 1
                    pot += tempallin
                    sidepot += player.totalamount()-tempallin
                    sidepotplayers.add(player.name)

                else:
                    lessallin = player.totalamount()
                    call = lessallin
                    temp = tempallin-lessallin
                    temp *= allincount
                    sidepot = temp
                    tempallin = lessallin * allincount
                    pot += lessallin - temp


            player.allin()
            break
        else:
            print("Please enter a valid choice.")


def aibet(player):
    global call, pot, tempcall, tempallin, sidepot, lessallin, allincount, sidepotplayersv #, players
    #current bet total, call count, player.chip1 -= 1(for anti, don't put into this function)
    #if temp = -1, it means player has folded, must be removed
    if sidepot > 0:
        print(f"Pot: {pot}\nCall: {call}\nSide Pot:{sidepot}")
    else:
        print(f"Pot: {pot}\nCall: {call}")
    player.displaychips()
    while True:
        print("Do you want to call, fold, raise, or go all in?")
        response = player.decidemove(pot,call,river, allincount)
        print(response)
        if response == "call":
            amount = player.take(call)
            tempcall += 1
            if amount == -1:
                fold(player)
            else:
                pot += amount
            break
        elif len(response) > 6:
            temp, response = response.split(" ")
            response = int(response)
            if response + call <= player.totalamount():
                call = response + call
                pot += player.take(call)
                print(f"Pot: {pot}\nCall: {call}")
                tempcall = 1
                break

        elif response[0] == "r":
                response = response.split(" ")
                digit = int(response[1])
                pot += digit
                call += digit

        elif response == "fold":
            fold(player)
            tempcall += 1
            break
        elif response == "all in" and player.totalamount() > 0:
            tempcall += 1
            if tempallin == 0:
                pot += player.totalamount()
                call = player.totalamount()
                allincount += 1
                tempallin = player.totalamount()
            else:
                if player.totalamount() > tempallin:
                    allincount += 1
                    pot += tempallin
                    sidepot += player.totalamount()-tempallin
                    sidepotplayers.add(player.name)

                else:
                    lessallin = player.totalamount()
                    call = lessallin
                    temp = tempallin-lessallin
                    temp *= allincount
                    sidepot = temp
                    tempallin = lessallin * allincount
                    pot += lessallin - temp


            player.allin()
            break
        else:
            print("Please enter a valid choice.")


def winner(river):
    global pot ,players, sidepot, sidepotplayers
    tie = []
    sidepottie = []
    playerrank = 0
    print(len(players))
    for i in range(len(players)):
        players[i].decode(river)
        if players[playerrank].rank < players[i].rank:
            playerrank = i

        elif players[playerrank].rank == players[i].rank:
            if players[playerrank].pokerhand == players[i].pokerhand:
                tie.append(playerrank)
                tie.append(i)

            else:
                for x, y in zip(players[playerrank].pokerhand, players[i].pokerhand):
                    if x > y:
                        break
                    elif y > x:
                        playerrank = i
                        break
    if len(tie) != 0:
        if players[playerrank].rank > players[tie[0]].rank:
            players[playerrank].get(pot)
            print(f"{players[playerrank].name} has won the pot.")

        else:
            tie = set(tie)
            pot = pot//len(tie)

            for i in tie:
                players[i].get(pot)


    pot = 0
    spp = []
    spprank = -1
    if sidepot != 0:
        for i in range(len(players)):
            for j in range(len(sidepotplayers)):
                if players[i].name == sidepotplayers[j].name:
                    spp.append(i)
        for i in spp:
            if players[spprank].rank < players[i].rank:
                spprank = i

            else:
                if players[playerrank].rank == players[i].rank:
                    if players[playerrank].pokerhand == players[i].pokerhand:
                        sidepottie.append(playerrank)
                        sidepottie.append(i)
                    else:
                        for x, y in zip(players[playerrank].pokerhand, players[i].pokerhand):
                            if x > y:
                                break
                            elif y > x:
                                spprank = i
                                break

        if players[playerrank].rank > players[sidepottie[0]].rank:
            players[playerrank].get(sidepot)
            print(f"{players[playerrank].name} has won the side pot.")

        else:
            sidepottie = set(sidepottie)
            sidepot = sidepot // len(sidepottie)
            for i in sidepottie:
                players[i].get(sidepot)


def nextround():
    global tempcall, call, pot, sidepot, tempallin, lessallin, allincount, deck, allplayers, players
    river.clear()
    folded = False
    tempcall = 0
    call = 1
    pot = 0
    sidepot = 0
    tempallin = 0
    lessallin = 0
    allincount = 0
    sidepotplayers.clear()
    deck = Deck
    players = allplayers.copy()
    for i in allplayers:
        print(i.name, i.totalamount())
        if i.totalamount() > 0:
            i.reset()
        else:
            players.remove(i)
    allplayers = players.copy()

    print(players)




def setup():
    global call, tempcall, players, allplayers, deck, river, folded
    deck = Deck()
    while True:
        name = input("What is your name?")
        stimes = input("How many times would you like the deck to be shuffled?")
        if stimes.isnumeric():
            deck.shuffle(int(stimes))
            break
        else:
            print("Please enter a number")
    players.append(Player(name))
    names = ["Joe", "Smith", "Todd", "Jill", "Hunter", "Juliana", "Chris", "Jessica", "Nicole"]
    for i in range(4):
        players.append(Player(random.choice(names)))
        names.remove(players[i+1].name)

    allplayers = players.copy()


def game():
    global call, tempcall, players, allplayers, deck, river, folded
    deck = Deck()
    for i in range(2):
        for player in players:
            player.draw(deck)
    # game loop
    river.append(deck.drawCard())
    while True:
        tempcall = 0
        if len(river) == 5:
            break
        tempcount = 0
        for i in players:
            if i.allincheck:
                tempcount +=1
        if tempcount == len(players):
            for j in range(5-len(river)):
                river.append(deck.drawCard())
            print("River: ")
            for i in range(len(river)):
                if i != 4:
                    print(river[i].show(), end=", ")
                else:
                    print(river[i].show())
            break
        run = True
        while run:
            for player in players:
                if tempcall < len(players):
                    player.showHand()
                    if players.index(player) == 0 and folded == False:
                        bet(player)
                    else:
                        aibet(player)
                    print(tempcall)
                else:
                    run = False
                    break
        river.append(deck.drawCard())
        print("River: ")
        for i in range(len(river)):
            if i != 4:
                print(river[i].show(), end=", ")
            else:
                print(river[i].show())

        call = 0
        print("")

    winner(river)

setup()
while True:
    game()
    print('NEW ROUND STARTING\n')
    nextround()




