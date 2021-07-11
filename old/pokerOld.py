import time
import csv
import numpy as np
#from numba import jit
t0 = time.time()

def suits():
    suits = "CSHD"
    deck = []
    for i in suits:
        for j in range(1,14):
            deck.append(i+str(j))
    return deck

def filterAvailable(set,startingCards,possibleHands,position):
    for combo in set:
        if startingCards[0] in combo and startingCards[1] in combo:
            possibleHands[position].append(combo)

def innerHighCardSort(i):
    return int(i[:-1])
def outerHighCardSort(i):
    temp = []
    for value in i:
        temp.append(int(value[:-1]))
    return temp

def combination():
    suits = "CDHS"
    deck = []
    singlePair = []
    doublePair = []
    triple = []
    quadruple = []
    fullHouse = []
    flush = []
    straight = []
    straightFlush = []
    highCard = []
    for i in suits:
        for j in range(2, 15):
            deck.append(str(j)+i)

    for i in range(0,48):
        print(i)
        for j in range(i+1,49):
            for k in range(j+1,50):
                for l in range(k+1,51):
                    for m in range(l+1,52):
                        hand = [deck[i],deck[j],deck[k],deck[l],deck[m]]
                        tempNumDic = {}
                        #tempNumDic produces a dictionary which tracks frequency of number
                        for value in hand:
                            num = int(value[:-1])
                            tempNumDic[num] = tempNumDic.get(num, 0) + 1
                        numbFreq = []
                        #numbFreq produces a list of the frequency of numbers without the associated dictionary like in tempNumDic
                        for key in tempNumDic:
                            numbFreq.append(tempNumDic[key])
                            numbFreq.sort()
                        #Sortet smallest => highest
                        #sort defintions
                        def innerRepeats(i):
                            return tempNumDic[i],i

                        # Sort the hand, first by frequency and then by number
                        def sortedHand():
                            sortHand = []
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            for number in newCombo:
                                for index in np.where(np.array(newCombo) == number)[0]:
                                    sortHand.append(hand[index])
                            return sortHand

                        #@jit(nopython=True)
                        #single pair
                        if numbFreq == [1, 1, 1, 2]:
                            sortHand = sortedHand()
                            singlePair.append(sortHand)
                        #double pair
                        elif numbFreq == [1, 2, 2]:
                            sortHand = sortedHand()
                            doublePair.append(sortHand)
                        #triple
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
                            tempSuitSet = set()
                            numberOnly = []
                            #numberOnly creates a list with only the numbers
                            #tempSuitSet produces a set with only the suits of each card
                            for value in hand:
                                suit = value[-1:]
                                num = value[:-1]
                                tempSuitSet.add(suit)
                                numberOnly.append(int(num))
                            numberOnly.sort()
                            if len(tempSuitSet) == 1:
                                if numberOnly[1] == numberOnly[0] + 1 and numberOnly[2] == numberOnly[0] + 2 and numberOnly[3] == numberOnly[0] + 3 and numberOnly[4] == numberOnly[0] + 4:
                                    straightFlush.append(hand)
                                elif numberOnly == [2, 3, 4, 5, 14]:
                                    # modHand is a new temporary hand to change the value of 14 to 1
                                    modHand = hand[:-1]
                                    newCard = hand[-1][0]+'1' # take the suit + 1
                                    # add the new card to the beginning
                                    modHand.insert(0,newCard)
                                    straightFlush.append(modHand)
                                else:
                                    hand.sort(key=innerHighCardSort)
                                    flush.append(hand)
                            else:
                                if numberOnly[1] == numberOnly[0] + 1 and numberOnly[2] == numberOnly[0] + 2 and numberOnly[3] == numberOnly[0] + 3 and numberOnly[4] == numberOnly[0] + 4:
                                    straight.append(hand)
                                elif numberOnly == [2, 3, 4, 5, 14]:
                                    # modHand is a new temporary hand to change the value of 14 to 1
                                    modHand = hand[:-1]
                                    newCard = hand[-1][0]+'1' # take the suit + 1
                                    # add the new card to the beginning
                                    modHand.insert(0,newCard)
                                    straight.append(modHand)
                                else:
                                    hand.sort(key=innerHighCardSort)
                                    highCard.append(hand)


    #Hierarchy
    hierarchy = [straightFlush, quadruple, fullHouse, flush, straight, triple, doublePair, singlePair, highCard]

    print(len(singlePair),len(doublePair),len(triple),len(quadruple),len(fullHouse),len(straight),len(flush),len(straightFlush),len(highCard))


    '''
    startingCards = ["14C","13C"]
    possibleHands = [[],[],[],[],[],[],[],[],[]]
    totalHands = 0
    for i in range(0,9):
        filterAvailable(hierarchy[i],startingCards,possibleHands,i)
        print(len(hierarchy[i]))
        totalHands += len(possibleHands[i])
    for sets in possibleHands:
        pass
        #print(round((len(sets)/totalHands)*100,4))
    '''
# combination()
combination()



tf = time.time()
print(tf-t0)
