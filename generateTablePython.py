#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""
# This python file produces a csv file containing the relative strength of each individual hand.
# Can use optimisation, however still runs in ~45 seconds.

# Import the necessary packages
#------------------------------
import time
import csv
import numpy as np
import operator as op
#------------------------------
# Set the starting time
t0 = time.time()

# Define the card class containing a number and a suit
class card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

# This function produces an array containing all the cards in the deck
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

# Sorting algorithms for later
#-----------------------------
def innerHighCardSort(i):
    return i.number

def outerHighCardSort(i):
    temp = []
    for value in i:
        temp.append(i.number)
    return temp
#-----------------------------


def combination(deck):
    # deck is of numpy array type
    # Define the lists which contain a 'Class' of poker hands
    singlePair = []
    doublePair = []
    triple = []
    quadruple = []
    fullHouse = []
    flush = []
    straight = []
    straightFlush = []
    highCard = []

    # Loop through every combination of cards in the deck
    for i in range(0,48):
        for j in range(i+1,49):
            for k in range(j+1,50):
                for l in range(k+1,51):
                    for m in range(l+1,52):
                        # Create a hand containing 5 cards
                        hand = [deck[i],deck[j],deck[k],deck[l],deck[m]]
                        # Remeber that a card has a number attribute so create a deck with only the numbers
                        numberOnly = [card.number for card in hand]

                        #numFreqDic produces a dictionary which tracks frequency of number
                        numFreqDic = {}
                        for value in hand:
                            num = value.number
                            numFreqDic[num] = numFreqDic.get(num, 0) + 1
                        #numbFreq produces a list of the frequency of numbers without the associated dictionary like in numFreqDic
                        numbFreq = []
                        for key in numFreqDic:
                            numbFreq.append(numFreqDic[key])
                            numbFreq.sort()
                        #Sort smallest => highest

                        #sort defintions
                        def innerRepeats(i):
                            # Sort first by the frequency then by the card number
                            return numFreqDic[i],i

                        # Returns a hand containing 'card' class ordered by the frequency then card number
                        def sortedHand():
                            sortHand = []
                            # This creates an array of card numbers, ordered.
                            newCombo = sorted(numFreqDic,key=innerRepeats)
                            # For every number find the index of this card in number only and add that card to the sorted hand
                            for number in newCombo:
                                for index in np.where(np.array(numberOnly) == number)[0]:
                                    sortHand.append(hand[index])
                            return sortHand

                        #single pair
                        # These numbFreq are unique to a specific hand
                        if numbFreq == [1, 1, 1, 2]:
                            sortHand = sortedHand()
                            singlePair.append(sortHand)
                        #double pair
                        elif numbFreq == [1, 2, 2]:
                            sortHand = sortedHand()
                            doublePair.append(sortHand)

                        #three of a kind
                        elif numbFreq == [1, 1, 3]:
                            sortHand = sortedHand()
                            triple.append(sortHand)
                        #four of a kind
                        elif numbFreq == [1, 4]:
                            sortHand = sortedHand()
                            quadruple.append(sortHand)
                        #full house
                        elif numbFreq == [2, 3]:
                            sortHand = sortedHand()
                            fullHouse.append(sortHand)
                        #straight, flush, straight flush, and high card remaining
                        else:
                            # Define a set type containg only the suits
                            # As it is a set no repeats are counted
                            suitSet = set([card.suit for card in hand])

                            # sort numberOnly
                            numberOnly.sort()
                            # If the length of the set is only 1 then we know all cards have same suit and thus a sort of flush
                            if len(suitSet) == 1:
                                # This simply filters through hands which follow a sequence and therefore a straight.
                                if numberOnly[1] == numberOnly[0] + 1 and numberOnly[2] == numberOnly[0] + 2 and numberOnly[3] == numberOnly[0] + 3 and numberOnly[4] == numberOnly[0] + 4:
                                    straightFlush.append(hand)
                                # Straights can also be built with aces acting as 1 so here we make sure we don't forget about them!
                                elif numberOnly == [2, 3, 4, 5, 14]:
                                    # Add a card with the same suit as the ace but with a number = 1
                                    hand.insert(0,card(hand[-1].suit,1))
                                    # Remove the last wrong ace card in the hand
                                    hand = hand[:-1]
                                    straightFlush.append(hand)
                                else:
                                    hand.sort(key=innerHighCardSort)
                                    flush.append(hand)
                            # Just the same as with the flushes... but instead called straights and highcards
                            else:
                                if numberOnly[1] == numberOnly[0] + 1 and numberOnly[2] == numberOnly[0] + 2 and numberOnly[3] == numberOnly[0] + 3 and numberOnly[4] == numberOnly[0] + 4:
                                    straight.append(hand)
                                elif numberOnly == [2, 3, 4, 5, 14]:
                                    # Same process as for straight flush
                                    hand.insert(0,card(hand[-1].suit,1))
                                    hand = hand[:-1]
                                    straight.append(hand)
                                else:
                                    hand.sort(key=innerHighCardSort)
                                    highCard.append(hand)



    # Now we sort the hands within a certain group/type
    # Probably worth writing neater (looping or functions) but this works and I'm not complaining.
    # for each group the number of the most important card is compared then the next one until all is sorted
    highCard.sort(key = lambda x: (x[4].number,x[3].number,x[2].number,x[1].number,x[0].number),reverse = True)
    singlePair.sort(key = lambda x: (x[3].number,x[2].number,x[1].number,x[0].number),reverse = True)
    doublePair.sort(key = lambda x: (x[4].number,x[2].number,x[0].number),reverse = True)
    triple.sort(key = lambda x: (x[2].number,x[1].number,x[0].number),reverse = True)
    straight.sort(key = lambda x: (x[4].number,x[3].number,x[2].number,x[1].number,x[0].number),reverse = True)
    flush.sort(key = lambda x: (x[4].number,x[3].number,x[2].number,x[1].number,x[0].number),reverse = True)
    fullHouse.sort(key = lambda x: (x[2].number,x[0].number),reverse = True)
    quadruple.sort(key = lambda x: (x[1].number,x[0].number),reverse = True)
    straightFlush.sort(key = lambda x: (x[4].number,x[3].number,x[2].number,x[1].number,x[0].number),reverse = True)

    #Hierarchy
    # This simply groups all the types of hands together for simplicity in the next part
    hierarchy = [straightFlush, quadruple, fullHouse, flush, straight, triple, doublePair, singlePair, highCard]
    allHands = np.ndarray(0)
    for group in hierarchy:
        allHands = np.append(allHands,[group])

    print(len(allHands))
    return allHands

    # Edit 13/7/2021 Removed the save to csv function as it turns out to not be useful and instead this entire file will be loaded into the next part
    # Instead the flattened folder is returned

    '''# Print just to make sure I filter the correct cards which I do!
    for group in hierarchy:
        print(len(group))
    # Finally save the cards in a csv file
    # Note: Excel/LibreOffice Calc is unable to open the 2+ million lines of hands :(
    with open('pokerRankings.csv','w') as file:
        writer = csv.writer(file)
        for val in hierarchy:
            for hand in val:
                writer.writerow([str(val.number)+val.suit for val in hand])
    '''
# Call the function
# combination()
# Time the code.
# tf = time.time()
# print(tf-t0)
