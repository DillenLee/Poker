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
#-------------------------------------------------------------------------------
# Set the starting time
t0 = time.time()

# Generate the deck from the previous python file
deck = gtp.generateDeck()
# and get the cards from the previous file (does take ~45 secs)
allHands = gtp.combination(deck)

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
    for hand in allHands:
        if hole[0] in hand and hole[1] in hand:
            # Find the index of the specific hand
            freqOfHand += 1
            index = allHands.index(hand)
            print(index)
            # Now look for all the same value hand by checking adjacent numbers
            upperLimit = lowerLimit = index
            while np.all([card.number for card in allHands[index]] == [card.number for card in allHands[upperLimit]]):
                if upperLimit != 2598959:
                    upperLimit += 1
                else:
                    break
            while np.all([card.number for card in allHands[index]] == [card.number for card in allHands[lowerLimit]]):
                lowerLimit -= 1 # doesn't matter too much here because when lowerLimit = -1 that
                                # just means the last element of the list which is ofc not the same as 0th element!
            tieFreq = upperLimit - lowerLimit
            winFreq = 2598960 - upperLimit
            lossFreq = lowerLimit
            totalTie += freqToProb(tieFreq)
            totalWin += freqToProb(winFreq)
            totalLoss += freqToProb(lossFreq)
    totalWin = totalWin/freqOfHand
    totalLoss = totalLoss/freqOfHand
    totalTie = totalTie/freqOfHand
    return totalTie, totalWin, totalLoss

# Loop through all the possible combinations of the starting hands
hole = [deck[0],deck[1]]
print(hole)
print(calculateWLProb(hole))
'''
for i in range(0,51):
    for j in range(i+1,52):
        hole = [str(deck[i].number)+deck[i].suit,str(deck[j].number)+deck[j].suit]
'''



tf = time.time()
print(tf-t0)
