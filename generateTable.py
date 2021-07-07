#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""
# Project started on 29/6/2021

# The purpose of this Python file is to produce a numpy array containing the
# relative strength for each starting hand. This way when given the two starting
# hands, there is no need to recalculate the strengths. This will reduce
# computation time massively.

#-----------------------------
# Begin with importing packages
import numpy as np
import operator
import time

t0 = time.time()
#-----------------------------

# define a new class called 'card' which simply contains a suit and a number
class card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number


# First create the deck
def generateDeck():
    suits = 'CSHD'
    deck = np.ndarray(52,dtype=object)
    for i in range(52):
        # Take the modulo to get a repeating value between 1 and 13
        number = (i%13)+2
        # To find the suit we divide by 13 (4 equal slices)
        suit = suits[int(i/13)]
        # Now we assign the card to the deck
        deck[i] = card(suit,number)
    return deck

# Create a function which returns how many repeats of a number there is
def repeatedNumber(hand):
    # Removes the suit
    numberOnly = [val.number for val in hand]
    # Creates a dictionary of the frequencies
    # Since this takes time look into structured lists in numpy
    freq = dict.fromkeys(numberOnly)

    repeats = np.ndarray(len(freq))
    for i,key in enumerate(freq):
        repeats[i] = freq[key]

    return freq,repeats

# Create a function which returns how many repeats of suits
def repeatedSuits(hand):
    suitsOnly = [val.suit for val in hand]
    suitsOnly = list(dict.fromkeys(suitsOnly))
    length = len(suitsOnly)
    return length


# Create a function to produce every single hand possible
def combinations(deck):         #deck is of type array
    # Create empty numpy arrays
    highCard = single = double = threeOAK = straight = flush = fullHouse = fourOAK = straightFlush = np.ndarray((0),dtype=object)


    index = 0
    for i in range(0,48):
        for j in range(i+1,49):
            for k in range(j+1,50):
                for l in range(k+1,51):
                    for m in range(l+1,52):
                        # Create a hand containing the 5 cards
                        hand = [deck[i],deck[j],deck[k],deck[l],deck[m]]
                        # And add them to the allHands array
                        # allHands[index] = hand


                        # Now we also want to categorise each hand
                        numbRepeatsDic,numbRepeats = repeatedNumber(hand)
                        suitRepeats = repeatedSuits(hand)      #Takes ~3 seconds

                        #Single pair
                        if len(numbRepeats) == 4:
                            index += 1
                            # sort the hand by asending order
                            hand = sorted(hand, key = lambda card: card.number, reverse=True)
                            single = np.append(single,hand)
                            # print([val.number for val in single[index]])
                            # now sort the big single list

                        # double pair
                        elif np.any(numbRepeats == 2) and len(numbRepeats) == 3:
                            double = np.append(double,hand)
                        #three of a kind
                        elif np.any(numbRepeats == 3) and len(numbRepeats) == 3:
                            threeOAK = np.append(threeOAK,hand)
                        #four of a kind
                        elif np.any(numbRepeats==4):
                            fourOAK = np.append(fourOAK,hand)
                        #full house
                        elif np.all(numbRepeats >= 2):
                            fullHouse = np.append(fullHouse,hand)

    # print(len(single),len(double),len(threeOAK),len(fourOAK),len(fullHouse))



    return



print(combinations(generateDeck()))
print(time.time()-t0)
