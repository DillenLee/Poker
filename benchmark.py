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

#To benchmark certain code snippets

import timeit
import numpy as np

statement = 'import numpy as np'

newCode = '''
def generateDeck():
    suits = 'CSHD'
    deck = np.ndarray(52,dtype=object)
    for i in range(52):
        # Take the modulo to get a repeating value between 1 and 13
        number = str((i%13)+1)
        # To find the suit we divide by 13 (4 equal slices)
        suit = suits[int(i/13)]
        # Now we assign the card to the deck
        deck[i] = suit+number
    return deck
'''
oldCode='''
def suits():
    suits = "CSHD"
    deck = []
    for i in suits:
        for j in range(1,14):
            deck.append(i+str(j))
    return np.array(deck)
'''
# print(timeit.timeit(newCode,statement,number=10000000))

arr = arr2 = np.ndarray(0,dtype=object)
print(np.append('1',arr))
print(arr2)
