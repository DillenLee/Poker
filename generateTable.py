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
# relative strength for each starting hand. Using this method when given the two starting
# cards, there is no need to recalculate the strengths. This will reduce
# computation time massively.

#-----------------------------
# Begin with importing packages
import numpy as np
import operator
import time
import csv

t0 = time.time()
#-----------------------------

# define a new class called 'card' which simply contains a suit and a number
class card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

# Create a simple function to estimate how much time is left
def timeLeft(t0,t1,remaining):
    return (t1-t0)*remaining

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
    freq = {}
    for item in numberOnly:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    repeats = np.array(list(freq.values()))
    # print(repeats)
    return freq,repeats

# Create a function which returns how many repeats of suits
def repeatedSuits(hand):
    suitsOnly = [val.suit for val in hand]
    suitsOnly = list(dict.fromkeys(suitsOnly))
    length = len(suitsOnly)
    return length

# This function will first order the cards based off the type of hand and then the relative strength within each type
def combinations(deck):         #deck is of type array
    # Create empty numpy arrays
    highCard = single = double = threeOAK = straight = flush = fullHouse = fourOAK = straightFlush = np.ndarray((0,5),dtype=object)


    index = 0
    t0 = time.time()
    for i in range(0,48):
        t1 = time.time()
        print(timeLeft(t0,t1,48-i))
        t0 = t1
        print(i)
        for j in range(i+1,49):
            for k in range(j+1,50):
                for l in range(k+1,51):
                    for m in range(l+1,52):
                        # Create a hand containing the 5 cards
                        hand = [deck[i],deck[j],deck[k],deck[l],deck[m]]
                        numberedHand = [val.number for val in hand]

                        # Now we also want to categorise each hand
                        numbRepeatsDic,numbRepeats = repeatedNumber(hand)
                        suitRepeats = repeatedSuits(hand)      #Takes ~3 seconds, returns number of repeats

                        # Required for later, sorts by frequency, then number
                        def innerRepeats(i):
                            return numbRepeatsDic[i],i

                        def duplicateSort():
                            sortHand = []
                            # sorting the cards gets a bit confusing and can be improved upon
                            # 1) Create an array (numberOnly) which sorts the numbers first by frequency,
                            #    then by size. This array contains only the unique numbers.
                            numberOnly = sorted(numbRepeatsDic, key=innerRepeats)
                            # 2) Starting from the smallest number, the indexes of cards containing the number is found
                            #    using np.where which produces an array.
                            for number in numberOnly:
                                for val in np.where(np.array(numberedHand) == number)[0]:   # the [0] index is to solve a weird thing with the formatting of np.where
                            # 3) A new list created previously (sortHand), will simply append the card from the hand
                            #    using the indexes just found
                                    sortHand.append(hand[val])
                            # finally return this new sorted hand!
                            return sortHand

                        #Single pair
                        if suitRepeats != 1:           # removes straight hands
                            sortHand = duplicateSort()
                            if len(numbRepeats) == 4:  # The condition is unique to single pair
                                # we append this sorted hand into the 'single' master array!
                                # single is an array containing all the single pair hands as elements
                                single = np.append(single,[sortHand],axis = 0)
                                # it works!
                            # double pair
                            elif np.any(numbRepeats == 2) and len(numbRepeats) == 3:
                                double = np.append(double,[sortHand],axis = 0)
                            #three of a kind
                            elif np.any(numbRepeats == 3) and len(numbRepeats) == 3:
                                threeOAK = np.append(threeOAK,[sortHand])
                            #four of a kind
                            elif np.any(numbRepeats == 4):
                                fourOAK = np.append(fourOAK,[sortHand])
                            #full house
                            elif np.all(numbRepeats >= 2):
                                fullHouse = np.append(fullHouse,[sortHand])
                            else:
                                # The remaining two are either high card or straight
                                hand = sorted(hand, key = lambda card: card.number)
                                # unbelievably hideous... but it works!
                                if hand[1].number == (hand[0].number)+1 and hand[2].number == (hand[0].number)+2 and hand[3].number == (hand[0].number)+3 and hand[4].number == (hand[0].number)+4:
                                    straight = np.append(straight,[hand],axis = 0)
                                # this is to catch ace, 2, 3, 4, 5 cases. Remember aces are counted as 14 in the deck
                                elif hand[0].number == 2 and hand[1].number == 3 and hand[2].number == 4 and hand[3].number == 5 and hand[4].number == 14:
                                    # reassign the number of the card
                                    hand[4].number = 1
                                    # then move the ace to the begininng
                                    hand = np.roll(hand,1)
                                    straight = np.append(straight,[hand],axis = 0)
                                else:
                                    highCard = np.append(highCard,[hand],axis = 0)

                        elif suitRepeats == 1:
                            # Exactly the same as above but instead its called 'Flush' and 'Straight flush'
                            hand = sorted(hand, key = lambda card: card.number)
                            if hand[1].number == (hand[0].number)+1 and hand[2].number == (hand[0].number)+2 and hand[3].number == (hand[0].number)+3 and hand[4].number == (hand[0].number)+4:
                                straightFlush = np.append(straightFlush,[hand],axis = 0)
                            elif hand[0].number == 2 and hand[1].number == 3 and hand[2].number == 4 and hand[3].number == 5 and hand[4].number == 14:
                                hand[4].number = 1
                                hand = np.roll(hand,1)
                                straightFlush = np.append(straightFlush,[hand],axis = 0)
                            else:
                                flush = np.append(flush,[hand],axis = 0)

    hierarchy = [straightFlush,fourOAK,fullHouse,flush,straight,threeOAK,double,single,highCard]
    with open('pokerRankings.csv','w') as file:
        writer = csv.writer(file)
        for val in hierarchy:
            for hand in val:
                writer.writerow([str(val.number)+val.suit for val in hand])
    print(len(single),len(double),len(threeOAK),len(fourOAK),len(fullHouse),len(straight),len(flush),len(straightFlush),len(highcard))



    



print(combinations(generateDeck()))
print(time.time()-t0)
