#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:29:35 2019

@author: adamrankin
"""
from data_crawler import DataCrawler
from mailer import Mailer


def main():
    crawler = DataCrawler()
    mailer = Mailer()
    mailer.add_dataframe_to_body('Stock Indices', crawler.get_indices(), crawler.index_url)
    mailer.add_dataframe_to_body('Commodities', crawler.get_commodities(), crawler.commodities_url)
    mailer.add_dataframe_to_body('Exchange Rates', crawler.get_exchange_rates(), crawler.exchange_url)
    mailer.add_dataframe_to_body('US Treasuries', crawler.get_treasuries(), crawler.treasuries_url)
    mailer.send_email()
    
    
    
if __name__=="__main__":
    main()