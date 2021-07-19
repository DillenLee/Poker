#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""
# This script will use the pokerRankings.csv file to find the relative strength
# between different starting hands and generate a probabilty table.

# Import the packages
#-------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import generateTablePython as gtp
import csv
import time
import os
#-------------------------------------------------------------------------------
# Set the starting time
t0 = time.time()

# Generate the deck from the previous python file
deck = gtp.generateDeck()
# and the aces with number = 1
oneAces = gtp.generateOneAce()
# now generate all the possilbe hands
allHands = gtp.combination(deck,oneAces)
allNumbers = [[card.number for card in hand] for hand in allHands]

tGenerate = time.time()
print('Time for set generation is ', tGenerate-t0)
# Just a quick calculation to find the probability given frequency
# It is assumed all cards drawn are equally likely
def freqToProb(freq):
    return 100*freq/2598960

def calculateWLProb(hole):
    freqOfHand = 0
    totalWin = 0
    totalLoss = 0
    totalTie = 0
    # In case of aces we need to be sure to add the aces with the number = 1 to the list
    if hole[0].number == 14:
        replaceSuit = hole[0].suit
        if replaceSuit == 'C':
            altCardA = oneAces[0]
        elif replaceSuit == 'S':
            altCardA = oneAces[1]
        elif replaceSuit == 'H':
            altCardA = oneAces[2]
        elif replaceSuit == 'D':
            altCardA = oneAces[3]

    if hole[1].number == 14:
        replaceSuit = hole[1].suit
        if replaceSuit == 'C':
            altCardB = oneAces[0]
        elif replaceSuit == 'S':
            altCardB = oneAces[1]
        elif replaceSuit == 'H':
            altCardB = oneAces[2]
        elif replaceSuit == 'D':
            altCardB = oneAces[3]

    if 'altCardA' in locals():
        if 'altCardB' in locals():
            # Both cards are aces
            condition = '(hole[0] in hand and hole[1] in hand) or (altCardA in hand and altCardB in hand) or (altCardA in hand and hole[1] in hand) or (hole[0] in hand and altCardB in hand)'
        else:
            # Only the first card is an ace
            condition = '(hole[0] in hand and hole[1] in hand) or (altCardA in hand and hole[1] in hand)'

    elif 'altCardB' in locals():
         # Only the second card is an ace
         condition = '(hole[0] in hand and hole[1] in hand) or (altCardB in hand and hole[0] in hand)'

    else:
        # Where both cards are not aces (the majority of the time)
        condition = '(hole[0] in hand and hole[1] in hand)'



    for index,hand in enumerate(allHands):
        if eval(condition):
            # Find the index of the specific hand
            freqOfHand += 1
            print(100*index/len(allHands))
            # Now look for all the same value hand by checking adjacent numbers
            upperLimit = lowerLimit = index
            mainCard = allNumbers[index]
            while np.all(mainCard == allNumbers[upperLimit]):
                if upperLimit != 2598959: # prevent index overflow
                    upperLimit += 1
                else:
                    break
            while np.all(mainCard == allNumbers[lowerLimit]):
                lowerLimit -= 1 # doesn't matter too much here because when lowerLimit = -1 that
                                # just means the last element of the list which is ofc not the same as 0th element!
            tieFreq = upperLimit - lowerLimit
            winFreq = 2598960 - upperLimit
            lossFreq = lowerLimit
            totalTie += freqToProb(tieFreq)
            totalWin += freqToProb(winFreq)
            totalLoss += freqToProb(lossFreq)
    # take the simple average as all cards/hands are equally likely
    totalTie = totalTie/freqOfHand
    totalWin = totalWin/freqOfHand
    totalLoss = totalLoss/freqOfHand
    return totalTie, totalWin, totalLoss



hole = [deck[12],deck[13]]
print([str(card.number)+card.suit for card in hole])
tie ,win ,loss = calculateWLProb(hole)
print(tie,win,loss)
# Loop through all the possible combinations of the starting hands
'''
for i in range(0,51):
    for j in range(i+1,52):
'''

tf = time.time()
print(tf-t0)
