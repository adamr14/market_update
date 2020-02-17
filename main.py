#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:29:35 2019

@author: adamrankin
"""
from data_crawler import DataCrawler
from mailer import Mailer
from plotter import Plotter
import os
import sys


def main():
    # Set directory
    os.chdir(os.path.dirname(sys.argv[0]))
    
    # instantiate different modules
    crawler = DataCrawler()
    plotter = Plotter()
    mailer = Mailer()
    
    # get treasury data
    treasury_data = crawler.get_treasuries()
    plotter.yield_curve(treasury_data)
    
    # get rid of stuff we dont want in the table
    treasury_data.pop('Last Week')
    treasury_data.pop('Last Month')
    
    # Add everything to email in order
    mailer.add_dataframe_to_body('US Treasuries', treasury_data, crawler.treasuries_url)
    mailer.add_image_to_body(plotter.ust_yield)
    mailer.add_dataframe_to_body('Stock Indices', crawler.get_indices(), crawler.index_url)
    mailer.add_dataframe_to_body('Commodities', crawler.get_commodities(), crawler.commodities_url)
    mailer.add_dataframe_to_body('Exchange Rates', crawler.get_exchange_rates(), crawler.exchange_url)
    
    # Send email
    mailer.send_email()
    
    
    
if __name__=="__main__":
    main()