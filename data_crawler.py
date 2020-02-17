#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:27:18 2019

@author: adamrankin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from datetime import date


class DataCrawler():
    
    def __init__(self):
        with open('./assets/config') as json_config:
            self.config = json.load(json_config)
        
    def get_indices(self):
        job = 'stock_indices'
        self.index_url = self.config[job]['url']
        keys = self.config[job]['keys']
        req = requests.get(self.index_url)
        data = req.text
        soup = BeautifulSoup(data, features="html.parser")
        prices=[]
        symbols=[]
        changes=[]
        names = []
        percentChanges=[]
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for symbol in srow.find_all('td', attrs={'class':'data-col0'}):
                    if symbol.text in keys.keys() and symbol.text not in symbols:
                        symbols.append(symbol.text)
                        names.append(keys[symbol.text] + ' ('+ symbol.text + ')')
                        for price in srow.find_all('td', attrs={'class':'data-col2'}):
                            prices.append(price.text)
                        for change in srow.find_all('td', attrs={'class':'data-col3'}):
                            changes.append(change.text)
                        for percentChange in srow.find_all('td', attrs={'class':'data-col4'}):
                            percentChanges.append(percentChange.text)
        return pd.DataFrame({'Prices': prices, 'Day Change': changes, '% Change': percentChanges}, index=names)
            
    def get_commodities(self):
        job = 'commodities'
        self.commodities_url = self.config[job]['url']
        keys = self.config[job]['keys']
        req = requests.get(self.commodities_url)
        data = req.text
        soup = BeautifulSoup(data, features="html.parser")
        prices=[]
        symbols=[]
        changes=[]
        percentChanges=[]
        names = []
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for symbol in srow.find_all('td', attrs={'class':'data-col0'}):
                    if symbol.text in keys.keys() and symbol.text not in symbols:
                        symbols.append(symbol.text)
                        names.append(keys[symbol.text] + ' ('+ symbol.text + ')')
                        for price in srow.find_all('td', attrs={'class':'data-col2'}):
                            prices.append(price.text)
                        for change in srow.find_all('td', attrs={'class':'data-col4'}):
                            changes.append(change.text)
                        for percentChange in srow.find_all('td', attrs={'class':'data-col5'}):
                            percentChanges.append(percentChange.text)
         
        return pd.DataFrame({'Prices': prices, 'Day Change': changes, '% Change': percentChanges}, index=names)
        
    def get_exchange_rates(self):
        job = 'exchange_rates'
        self.exchange_url = self.config[job]['url']
        keys = self.config[job]['keys']
        req = requests.get(self.exchange_url)
        data = req.text
        soup = BeautifulSoup(data, features="html.parser")
        prices=[]
        symbols=[]
        changes=[]
        names=[]
        percentChanges=[]
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for symbol in srow.find_all('td', attrs={'class':'data-col0'}):
                    if symbol.text in keys.keys() and symbol.text not in symbols:
                        symbols.append(symbol.text)
                        names.append(keys[symbol.text] + ' ('+ symbol.text + ')')
                        for price in srow.find_all('td', attrs={'class':'data-col2'}):
                            prices.append(price.text)
                        for change in srow.find_all('td', attrs={'class':'data-col3'}):
                            changes.append(change.text)
                        for percentChange in srow.find_all('td', attrs={'class':'data-col4'}):
                            percentChanges.append(percentChange.text)
         
        return pd.DataFrame({'Ratio': prices, 'Day Change': changes, '% Change': percentChanges}, index=names)
        
    def get_treasuries(self):
        job = 'us_treasuries'
        self.treasuries_url = self.config[job]['base_url'] + str(date.today().year)
        
        names = []
        rows = []
        
        #
        # If feb or jan get the previous year too
        #
        if date.today().month <= 2:
            req = requests.get(self.config[job]['base_url'] + str(date.today().year-1))
            data = req.text
            soup = BeautifulSoup(data, features="html.parser")
            table = soup.find('table', attrs={'class':'t-chart'})
            for row in table.find_all('tr'):
                rows.append(row)
                
        req = requests.get(self.treasuries_url)
        data = req.text
        soup = BeautifulSoup(data, features="html.parser")
        table = soup.find('table', attrs={'class':'t-chart'})
        for name in table.find_all('th'):
            names.append(name.text)
        for row in table.find_all('tr'):
            rows.append(row)
        names.pop(0)
        curr_prices = self.__parse_t_row(rows[-1])
        yesterday_prices = self.__parse_t_row(rows[-2])
        last_week_prices = self.__parse_t_row(rows[-6])
        last_month_prices = self.__parse_t_row(rows[-23])
        changes = []
        i=0
        for price in curr_prices:
            changes.append(round(price - yesterday_prices[i], 2))
            i+=1
        return pd.DataFrame({'Current Yield': curr_prices, 
                             'Day Change': changes,
                             'Last Week': last_week_prices,
                             'Last Month': last_month_prices
                             }, index=names)

    #
    # Parses a row of treasuries
    #    
    def __parse_t_row(self, row):
        i=0
        prices = []
        for data in row.find_all('td'):
            if i!=0:
                prices.append(float(data.text))
            i+=1
        return prices
    
