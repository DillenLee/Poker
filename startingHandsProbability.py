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

# Open the csv file
df = pd.read_csv('pokerRankings.csv',header=None)
# and convert to numpy array
allHands = df.to_numpy().tolist()
# Probably a faster way to do this but it works
allHandsOnlyNumber = [[card[:-1] for card in hand] for hand in allHands]

# Generate the deck from the previous python file
deck = gtp.generateDeck()

# Just a quick calculation to find the probability given frequency
# It is assumed all cards drawn are equally likely
def freqToProb(freq):
    return 100*freq/2598960

def calculateWLProb(hole):
    freqOfHand = 0
    totalWin = 0
    totalLoss = 0
    for hand in allHands:
        if hole[0] in hand and hole[1] in hand:
            # Find the index of the specific hand
            freqOfHand += 1
            index = allHands.index(hand)
            print(index)
            # Now look for all the same value hand by checking adjacent numbers
            upperLimit = index+1
            lowerLimit = index-1
            while np.all(allHandsOnlyNumber[index] == allHandsOnlyNumber[upperLimit]):
                upperLimit += 1
            while np.all(allHandsOnlyNumber[index] == allHandsOnlyNumber[lowerLimit]):
                lowerLimit -= 1
            tieFreq = upperLimit - lowerLimit
            winFreq = 2598960 - upperLimit
            lossFreq = lowerLimit
            totalWin += freqToProb(winFreq)
            totalLoss += freqToProb(lossFreq)
    totalWin = totalWin/freqOfHand
    totalLoss = totalLoss/freqOfHand
    totalTie = freqToProb(lossFreq)
    return totalTie, totalWin, totalLoss

# Loop through all the possible combinations of the starting hands
hole = [str(deck[0].number)+deck[0].suit,str(deck[1].number)+deck[1].suit]
print(calculateWLProb(hole))
'''
for i in range(0,51):
    for j in range(i+1,52):
        hole = [str(deck[i].number)+deck[i].suit,str(deck[j].number)+deck[j].suit]
'''



tf = time.time()
print(tf-t0)
