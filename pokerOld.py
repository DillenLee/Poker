import time
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
    list=[]
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
        jVal = i + 1
        for j in range(jVal,49):
            kVal = j + 1
            for k in range(kVal,50):
                lVal = k + 1
                for l in range(lVal,51):
                    mVal = l + 1
                    for m in range(mVal,52):
                        combination = [deck[i],deck[j],deck[k],deck[l],deck[m]]
                        list.append(combination)
                        tempNumDic = {}
                        #tempNumDic produces a dictionary which tracks frequency of same number card
                        for value in combination:
                            num = int(value[:-1])
                            tempNumDic[num] = tempNumDic.get(num, 0) + 1
                        temp = []
                        #temp produces a list of the frequency of numbers without the associated dictionary like in tempNumDic
                        for key in tempNumDic:
                            temp.append(tempNumDic[key])
                            temp.sort()
                        #Sortet smallest => highest
                        #sort defintions
                        def innerRepeats(i):
                            return tempNumDic[i],i

                        #@jit(nopython=True)
                        #single pair
                        if temp == [1, 1, 1, 2]:
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            newCombo.append(newCombo[3])
                            singlePair.append(newCombo)
                        #double pair
                        elif temp == [1, 2, 2]:
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            newCombo.extend([newCombo[1],newCombo[2]])
                            newCombo.sort(key=innerRepeats)
                            doublePair.append(newCombo)
                        #triple
                        elif temp == [1, 1, 3]:
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            newCombo.extend([newCombo[2],newCombo[2]])
                            newCombo.sort(key=innerRepeats)
                            triple.append(newCombo)
                        #four of a kind
                        elif temp == [1, 4]:
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            newCombo.extend([newCombo[1],newCombo[1],newCombo[1]])
                            newCombo.sort(key=innerRepeats)
                            quadruple.append(newCombo)
                        #full house
                        elif temp == [2, 3]:
                            newCombo = sorted(tempNumDic,key=innerRepeats)
                            newCombo.extend([newCombo[0],newCombo[1],newCombo[1]])
                            newCombo.sort(key=innerRepeats)
                            fullHouse.append(newCombo)
                        #straight, flush, straight flush, and high card remaining
                        else:
                            tempSuitSet = set()
                            temp = []
                            #temp creates a list with only the numbers
                            #tempSuitSet produces a set with only the suits of each card
                            for value in combination:
                                suit = value[-1:]
                                num = value[:-1]
                                tempSuitSet.add(suit)
                                temp.append(int(num))
                            temp.sort()
                            if len(tempSuitSet) == 1:
                                flush.append(combination)
                            if temp[1] == temp[0] + 1 and temp[2] == temp[0] + 2 and temp[3] == temp[0] + 3 and temp[4] == temp[0] + 4 or temp == [2, 3, 4, 5, 14]:
                                straight.append(combination)
                            elif len(tempSuitSet) != 1:
                                combination.sort(key=innerHighCardSort)
                                highCard.append(combination)

    for combination in straight:
        if combination in flush:
            straightFlush.append(combination)
    for combination in straightFlush:
        flush.remove(combination)
        straight.remove(combination)



    #Hierarchy
    hierarchy = [highCard, singlePair, doublePair, triple, straight, flush, fullHouse, quadruple, straightFlush]

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

# combination()
print(suits())



tf = time.time()
print(tf-t0)
