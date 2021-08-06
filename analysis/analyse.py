#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""

# Run some analysis on the data
# ------------------------------------------------------------------------------
# Import the necessary packages
import matplotlib.pyplot as plt
import numpy as np

# Starting hand cards data
# import the probabiltiy of winning
win = np.loadtxt("/home/dillen/PersonalProjects/Poker/data/startingHands.csv" ,dtype=float, delimiter = ',',usecols=3)
# define the bin range (and also width)
bins = np.arange(0,100,2)

# Plot the data on a histogram
plt.hist(win, bins = bins)
plt.xlabel("Probability of winning")
plt.ylabel("Frequency")
plt.show()


# Sort the data
win.sort()
plt.plot(win)
plt.show()
