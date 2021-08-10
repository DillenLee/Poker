#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""
# This python file will be generate the game

# Import the necessary python files
#-------------------------------------------------------------------------------
import numpy as np
import generateTablePython as gtp
import random as rand
import time
import pandas as pd
import copy
import itertools as it
import os
#-------------------------------------------------------------------------------

# Create a new class called player with all the appropriate atributes.
# personalBet describes the amount a player has bet in one game of betting
class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.cards = []
        self.personalBet = 0
        self.totalInvested = 0
        self.hasRaised = False

    # a method to update the money

    def bet(self,amount):
        # Doesn't check if amount is > money
        self.money = (self.money-amount)
        # Whenever bet just add the amount to what is currently betting
        self.personalBet += amount
        # Also add the total bet per game
        self.totalInvested += amount


    # a method to clear the personalBet attribute
    def clearPersonalBet(self):
        self.personalBet = 0

# Begin the game by creating the deck
deck = gtp.generateDeck()

# Define some basic functions
#-------------------------------------------------------------------------------
def call(player,currentBet,pot,mode):
    currentAmount = player.personalBet
    difference = currentBet - currentAmount
    player.bet(difference)
    pot += difference
    if mode == 'v':
        print(player.name, "called")
        print(player.name, "is currently betting", player.personalBet)

    return pot

def fold(player, players, mode):
    if mode == 'v':
        print(player.name, "folded")
        print(player.name, "is currently betting", player.personalBet)
    players.remove(player)


# Amount is defined as the amount above the currentBet
def raiseBet(player,currentBet,amount,pot, mode):
    currentPlayerBet = player.personalBet
    totalBet = (currentBet - currentPlayerBet) + amount
    player.bet(totalBet)
    pot += totalBet
    if mode == 'v':
        print(player.name, "raised")
        print(player.name, "is currently betting", player.personalBet)
    return pot, totalBet
#-------------------------------------------------------------------------------

# Create the algorithms
#-------------------------------------------------------------------------------
def holeDecide(player,currentBet,players,holesDF,pot,count,index,limit,mode):
    holeCards = player.cards
    # Sort the hole cards to find their win/loss prob quickly
    # First by the order of CSHD, then the number low ->
    order = 'CSHD'
    holeCards.sort(key = lambda x: (order.index(x.suit),x.number))
    handData = holesDF[(holesDF[0] == holeCards[0].comb) & (holesDF[1] == holeCards[1].comb)].to_numpy()[0]

    prob = handData[3]

    if prob < 50:
        # when you fold the only change is returning the index-1 as the player is removed from the list, so the next player inherits the same index.
        fold(player,players,mode)
        return pot, currentBet, count, index-1, limit

    elif prob > 50 and prob < 55:
        # Calling only changes the pot size in the game, the personalBet should be increased
        if player.money+player.personalBet >= currentBet:
            pot = call(player,currentBet,pot,mode)
        else:
            fold(player,players,mode)
            return pot, currentBet, count, index-1, limit
        # Verbose mode
        return pot, currentBet, count, index, limit

    elif prob > 55:
        # Can't raise twice in the same game
        if player.hasRaised == False:
            # Raising changes the pot size and the current bet as well as the count
            if player.money >= 100:
                pot, currentBet = raiseBet(player,currentBet,100,pot,mode)
            else:
                pot, currentBet = raiseBet(player,currentBet,player.money,pot,mode)
            player.hasRaised = True
            # Reset the count (and also limit) to allow for everyone to have a chance to bet
            count = 0
            limit = len(players)
            return pot, currentBet, count, index, limit
        else:
            if player.money+player.personalBet >= currentBet:
                pot = call(player,currentBet,pot,mode)
                return pot, currentBet, count, index, limit
            else:
                fold(player,players,mode)
                return pot, currentBet, count, index-1, limit

# def flopDecide(player, currentBet, players):

def randomChoice(player,currentBet,players,pot,count,index,limit,mode):
    # This is a function to just continue testing the program
    choice = rand.randint(1,2)
    if choice == 0:
        fold(player,players,mode)
        return pot, currentBet, count, index-1, limit
    elif choice == 1:
        # Calling only changes the pot size in the game, the personalBet should be increased
        if player.money+player.personalBet >= currentBet:
            pot = call(player,currentBet,pot,mode)
            return pot, currentBet, count, index, limit
        else:
            fold(player,players,mode)
            return pot, currentBet, count, index-1, limit
    elif choice == 2:
        # Can't raise twice in the same game
        if player.hasRaised == False:
            # Raising changes the pot size and the current bet as well as the count
            if player.money >= 100:
                pot, currentBet = raiseBet(player,currentBet,100,pot,mode)
            else:
                pot, currentBet = raiseBet(player,currentBet,player.money,pot,mode)

            player.hasRaised = True
            # Reset the count (and also limit) to allow for everyone to have a chance to bet
            count = 0
            limit = len(players)
            return pot, currentBet, count, index, limit
        else:
            if player.money+player.personalBet >= currentBet:
                pot = call(player,currentBet,pot,mode)
                return pot, currentBet, count, index, limit
            else:
                fold(player,players,mode)
                return pot, currentBet, count, index-1, limit

#-------------------------------------------------------------------------------

# Create some functions for calculating and showing percentages in progress bars :D
def generateProgressBar(player,totalMoney,maxBars = 50):
     ratio = player.money/totalMoney
     if ratio > 1:
         input('STOP ' + str(ratio))
     xBars = int(np.round(ratio*maxBars))
     oBars = maxBars - xBars

     progBar = '['
     for bar in range(0,xBars):
         progBar += '▰'
     for bar in range(0,oBars):
         progBar += '▱'
     progBar += ']'

     return progBar

# Create a function to generate the players for the game
def setUp(amtPlayers = 6, principle = 5000):
    # For fun, lets have a list of names to give the players some character
    names = ['Dillen', 'Nina', 'Kasper', 'Siebe', 'Mili', 'Evie', 'Paolo', 'Ambre', 'Chiara']
    players = []
    for i in range(amtPlayers):
        # Choose a random name
        nameIndex = rand.randint(0,len(names)-1)
        name = names[nameIndex]
        names.remove(name)
        players.append(Player(name,principle))

    return players


def main(mode = 'q'):
    # Call the set up function and create the players and remaining deck
    players = setUp()

    # Also import the csv file containing the data about the hole cards
    holesDF = pd.read_csv('data/startingHands.csv',header = None)

    # Set some starting conditions
    smallBlindIndex = 0
    bigBlindIndex = 1
    game = 0

    totalMoney = len(players)*5000

    # This clearing function will be repeated so it will be defined here
    def resetVariables(players, currentBet, count, limit, index):
        for player in players:
            player.clearPersonalBet()
            player.hasRaised = False
        # Reset the personalBet, count, limit, and index
        currentBet = 0
        count = 0
        limit = len(players)
        index = 0
        return players, currentBet, count, limit, index



    # Set the conditions for the game to continue playing
    # Which is set to the amount of players with money being > 2
    # playersInGame will be the amount of players still with money
    playersInGame = players.copy()
    while len(playersInGame) > 1:
        if mode == 'm':
            os.system('clear')
            # totalMoney = 0
            # for player in players:
            #     totalMoney += player.money

            for player in playersInGame:
                bar = generateProgressBar(player,totalMoney)
                print(player.name, bar ,player.money)

        for player in playersInGame:
            if player.money <= 0:
                playersInGame.remove(player)
                smallBlindIndex = (smallBlindIndex-1)%len(playersInGame)
                bigBlindIndex = (bigBlindIndex-1)%len(playersInGame)


        # If statement to make sure the game doesn't continue if we only have one player
        # Probably can be solved in a better way but it works
        if len(playersInGame) == 1:
            break


        players = playersInGame.copy()
        # This while loops allow the game to end before the showdown.
        # The loop does not mean anything in the physical game
        while True:
            # Set some starting conditions for each game
            currentBet = 0
            pot = 0

            for player in players:
                player.clearPersonalBet()
                player.totalInvested = 0

            # Shuffle the deck
            remainingDeck = deck
            np.random.shuffle(remainingDeck)

            # Deal the cards for the players
            for player in players:
                player.cards = [remainingDeck[0],remainingDeck[1]]
                remainingDeck = remainingDeck[2:]

            # Currently small blind is only 1 percent of the players money
            # smallBlind = players[smallBlindIndex].money*0.01
            smallBlind = 5
            pot += smallBlind
            players[smallBlindIndex].bet(smallBlind)
            # Big blind is usually twice the small blind

            bigBlind = smallBlind*2
            currentBet = bigBlind
            players[bigBlindIndex].bet(bigBlind)
            pot += bigBlind

            # Now we begin with the first round
            if mode == 'v':
                print([player.name for player in players])
            # The plus 1 is required to begin with the player after the big blind
            index = (bigBlindIndex+1)%len(players)
            # The limit and the count works together, the count increments every round until it hits the limit which is set to the length of the player.
            # Whenever someone raises, the limit changes (to the remaining amount of players) and the count resets.
            limit = len(players)
            count = 0


            while count < limit:
                if mode == 'v':
                    print('The current player is ',players[index].name)
                    print(count)
                    print(index)
                # holeDecide should return the pot size, currentBet, count, index, and limit
                pot, currentBet, count, index, limit = holeDecide(players[index],currentBet,players,holesDF, pot, count, index, limit,mode)
                if mode == 'v':
                    print('The current pot size is ',pot)
                if len(players) == 1:
                    break
                index = (index+1)%len(players)
                count += 1
            # check if there is a winner
            if len(players) == 1:
                # winner
                players[0].money += pot
                if mode == 'v':
                    print(players[0].name, 'wins by default!')
                smallBlindIndex = (smallBlindIndex + 1)%len(playersInGame)
                bigBlindIndex = (bigBlindIndex + 1)%len(playersInGame)
                game += 1
                break

            # Begin round 2, "the flop"
            # Clearing variables
            # As clearing the variables will be required for the next rounds a function will be defined
            players, currentBet, count, limit, index = resetVariables(players, currentBet, count, limit, index)

            # Then deal the next three cards
            flop = [remainingDeck[0],remainingDeck[1],remainingDeck[2]]
            # and remove the cards from the deck
            remainingDeck = remainingDeck[3:]
            #
            if mode == 'v':
                print('We have entered the second stage with',[player.name for player in players])
            while count < limit:
                if mode == 'v':
                    print('The current player is ',players[index].name)
                    print(count)
                    print(index)
                pot, currentBet, count, index, limit = randomChoice(players[index],currentBet,players, pot, count, index, limit,mode)
                if mode == 'v':
                    print('The current pot size is ',pot)
                if len(players) == 1:
                    break
                index = (index+1)%len(players)
                count += 1
            # check if there is a winner
            if len(players) == 1:
                # winner
                players[0].money += pot
                if mode == 'v':
                    print(players[0].name, 'wins by default!')
                smallBlindIndex = (smallBlindIndex + 1)%len(playersInGame)
                bigBlindIndex = (bigBlindIndex + 1)%len(playersInGame)
                game += 1
                break

            # Begin round 3, "the turn"
            # Clearing variables
            players, currentBet, count, limit, index = resetVariables(players, currentBet, count, limit, index)

            # Then deal the next card
            turn = [remainingDeck[0]]
            # and remove the card from the deck
            remainingDeck = remainingDeck[1:]
            #
            if mode == 'v':
                print('We have entered the third stage with',[player.name for player in players])
            while count < limit:
                if mode == 'v':
                    print('The current player is ',players[index].name)
                    print(count)
                    print(index)
                pot, currentBet, count, index, limit = randomChoice(players[index],currentBet,players, pot, count, index, limit, mode)
                if mode == 'v':
                    print('The current pot size is ',pot)
                if len(players) == 1:
                    break
                index = (index+1)%len(players)
                count += 1
                # check if there is a winner
            if len(players) == 1:
                # winner
                players[0].money += pot
                if mode == 'v':
                    print(players[0].name, 'wins by default!')
                smallBlindIndex = (smallBlindIndex + 1)%len(playersInGame)
                bigBlindIndex = (bigBlindIndex + 1)%len(playersInGame)
                game += 1
                break

            # Begin round 4, "the river"
            # Clearing variables
            players, currentBet, count, limit, index = resetVariables(players, currentBet, count, limit, index)

            # Then deal the next card
            river = [remainingDeck[0]]
            # and remove the card from the deck
            remainingDeck = remainingDeck[1:]

            if mode == 'v':
                print('We have entered the final stage with',[player.name for player in players])
            while count < limit:
                if mode == 'v':
                    print('The current player is ',players[index].name)
                    print(count)
                    print(index)
                pot, currentBet, count, index, limit = randomChoice(players[index],currentBet,players, pot, count, index, limit, mode)
                if mode == 'v':
                    print('The current pot size is ',pot)

                if len(players) == 1:
                    break
                index = (index+1)%len(players)
                count += 1
            # check if there is a winner
            if len(players) == 1:
                # winner
                players[0].money += pot
                if mode == 'v':
                    print(players[0].name, 'wins by default!')
                smallBlindIndex = (smallBlindIndex + 1)%len(playersInGame)
                bigBlindIndex = (bigBlindIndex + 1)%len(playersInGame)
                game += 1
                break

            # Now we enter the 'Showdown' phase
#-------------------------------------------------------------------------------
            # Define a function to return the best card for a given player
            def findBestHand(player):
                # List all the available cards to generate their best hand
                availableCards = player.cards + flop + turn + river
                allTupleCombinations = list(it.combinations(availableCards,5))
                # itertools generates the combinations in tuples, but lists are required so here it converts every hand from tuple to combination
                allListCombinations = [list(hand) for hand in allTupleCombinations]
                # Take the first card for the best
                bestHand = gtp.sortAllHands(allListCombinations)[0]

                return bestHand


            # This is a list of all the personal best hands to be compared
            allBestHands = []
            for player in players:
                allBestHands.append(findBestHand(player))

            # Now we want to find the best hand out of all the personal best hands
            winningHand = gtp.sortAllHands(allBestHands)[0]
            # Get the winner from the hand
            winningIndex = allBestHands.index(winningHand)
            winningPlayer = players[winningIndex]
#-------------------------------------------------------------------------------

            winningPlayer.money += pot
            if mode == 'v':
                print(winningPlayer.name, 'wins by showdown!')



            smallBlindIndex = (smallBlindIndex + 1)%len(playersInGame)
            bigBlindIndex = (bigBlindIndex + 1)%len(playersInGame)
            game += 1

            # Clear variables for next game
            players, currentBet, count, limit, index = resetVariables(players, currentBet, count, limit, index)

            # input()
            break
        print('Previous pot size', pot)
        print('Game ', game)
        time.sleep(0.05)

main('m')
