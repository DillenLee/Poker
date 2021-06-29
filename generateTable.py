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

# The purpose of this Python file is to produce an excel table containing the
# relative strength for each starting hand. This way when given the two starting
# hands, there is no need to recalculate the strengths. This will reduce
# computation time massively.

#-----------------------------
# Begin with importing packages
import numpy as np
import time

t0 = time.time()
#-----------------------------
# First create the deck
def generateDeck():
    # Not the way I would've liked it but it seems to be the fastest way
    suits = "CSHD"
    deck = []
    for i in suits:
        for j in range(1,14):
            deck.append(i+str(j))
    return np.array(deck)

# Create a function to produce every single hand possible
def combinations(deck):         #deck is of type array
    # There are ncr(52,5) = 2,598,960 different combinations of hands
    allHands = np.ndarray((5,2598960),dtype=object)
    for i in np.arange(2598960):
        j = i*5/2598960



print(generateDeck())
print(time.time()-t0)
