# Poker
## Introduction
Texas Hold'em is a game in the larger family of card games under the umbrella term of 'Poker'. This project aims to ultimately play Texas Hold'em by calculating the probabilities of each individual state (hand) in order to aid in decision making.
### Rules of the game
A quick summary of the rules of Texas Hold'em is written below:
Each player is first dealt two cards face down so that each player knows only their own cards. The player to the left of the dealer begins by betting a certain amount regardless of whether they like their cards (often called the small blind). The next player then doubles the small blind's bet (called the big blind). The player after them can then decide whether they would like to match the bet (and play on) or fold (and quit without losing anything). This continues on until everyone has either folded or matched. The dealer then deals three cards (called 'the flop') followed by a round of betting. This continues on with two more single card reveals (called 'the turn' and 'the river') until either one player remains (in which case they automatically win the pot) or we enter the 'showdown' phase of the game. In the showdown each player builds the strongest 5-card hand out of the available 7 cards (two personal cards and the five 'community' cards), with the winner being the one with the strongest hand. In the case of tied winners the pot is split.

[Source](https://en.wikipedia.org/wiki/Texas_hold_%27em)

### Poker hand ranking
The poker raking of the poker hands are shown below

<img src ='https://upload.wikimedia.org/wikipedia/commons/3/35/Poker_Hands.png' width = 500>

[Poker Hands, CellarDoor85 (Robert Aehnelt), licensed under CC BY-SA 3.0, via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Poker_Hands.png)

## Probability
Texas Hold'em is ultimately a 5-card hand game which means that there are ncr(52,5) = 2,596,980 different hand combinations. In the final 'showdown' phase there is, however, ultimately 7 cards available out of which the best 5 card hand is chosen. [To be continued]  

## Getting Started
This project aims to let algorithms play against each other. The main file in which this occurs is the pokerGame.py file which simulates 1 game of Texas Hold'em. The game is built into a function so it can be called and looped to play multiple games for data collection.

## Goals
The ultimage goal for this project is to produce algorithims which maximises the total outcome for a single player.

### Algorithms
There are a couple different strategies involved in the creation of algorithms, but they all rely on data regarding the state of their current available cards. A file for generating all the combination of 5-card and 7-card hands is required. From this data, the probability of winning for every starting card combination can be calculated. A list of possible strategies are listed below:
1. Bet high, but infrequent (Var. 1)
A common strategy is to bet infrequently (on good hands), but high. This can be implemented with a simple _probability of hand_> _certain probabilty_ or dynamically by optimising the pass probability over multiple games.
2. Asign a certain (monetary) value to every starting hand, and detirmine if it is worth continuing (given the pot size, and bet size). This method can also be optimised by changing the monetary value every round.
3. [... other stuff]

Checklist:
- [x] Generate all 5-card combination  
  Under generateTablePython.py
- [ ] Generate all 7-card combination
- [x] Generate data for starting combinations
  Under startingHandsProbability.py
- [ ] Create starting cards algorithm
  - [ ] For var. 1
    - [x] For a static case
    - [ ] For a dynamic case
  - [ ] For var. 2
  - [ ] For var. 3
- [ ] Create flop round algorithm
- [ ] Create turn round algorithm
- [ ] Create river round algorithm

## [Some more stuff]
