#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:04:30 2020

@author: adamrankin
"""

import matplotlib.pyplot as plt
import numpy as np

class Plotter():
    
    def __init__(self):
        self.ust_yield = 'UST_Yield.png'
    #
    # gets a pandas data frame of current treasury yield, day changes,
    # last week yield, and last month yield
    #
    def yield_curve(self, data):
        xticks = data.index.values
        xvals = np.array([1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360])
        plt.figure(figsize=(12,4))
        plt.xticks(xvals, xticks)
        plt.xticks(fontsize = 8, rotation=90)
        plt.plot(xvals, data['Current Yield'])
        plt.plot(xvals, data['Last Week'])
        plt.plot(xvals, data['Last Month'])
        plt.legend()
        plt.grid()
        plt.title('UST Yield Curve')
        plt.savefig('./attachments/' + self.ust_yield, dpi = 300)
        plt.close()
        return