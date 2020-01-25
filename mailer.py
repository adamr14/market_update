#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:20:15 2019

@author: adamrankin
"""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import date

class Mailer():
    
    def __init__(self):
        self.port = 465
        self.context = ssl.create_default_context()
        recipients=''
        while (recipients != 'test' and recipients != 'all'):
            recipients=input("Recipients (all or test): ")
        if recipients == 'all':
            self.__load_contacts()
        else:
            self.contacts = {'email@website.edu': 'Adam'}
        self.password=input("Password:")
        self.body_html=''
        self.body_text=''
        
    
    
    def send_email(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Daily Market Update for " + date.today().strftime("%m/%d/%Y")
        message["From"] = "dailymarketjournal@gmail.com"
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login("dailymarketjournal@gmail.com", self.password)
            for receiver in self.contacts.keys():
                message["To"] = receiver
                
                #
                # builds email as text
                #
                content_text='Hey ' + self.contacts[receiver] +',\n\n'
                content_text+='Here is your daily market update:\n\n\n'
                content_text+=self.body_text
                content_text+='\n\nAll data collected from Yahoo Finance\n\nTo unsubscribe, reply to this email indicating so'
                
                #
                # builds email in html
                #
                content_html="""\
                <html>
                    <body>
                        <p style="color:black;">Hey """ + self.contacts[receiver] +""", <br><br>
                        Here is your daily market update:</p>"""
                content_html+=self.body_html
                content_html+="""\
                        <p style="color:black;"><br><br>All data collected from Yahoo Finance and the Federal Reserve Website<br><br>
                        To Unsubscribe, reply to this email indicating so</p>
                    </body>
                </html>
                """
                part1 = MIMEText(content_text, "plain")
                part2 = MIMEText(content_html, "html")
                message.attach(part1)
                message.attach(part2)
                server.sendmail("dailymarketjournal@gmail.com", receiver, message.as_string())
                
    def add_dataframe_to_body(self, title, table, url):
        self.body_html+='<h2 style="color:black;"><a href=' + url + '>'+title+'</a></h2>'
        self.body_html+=table.to_html()
        self.body_text+= title + '\n'
        self.body_text+=table.to_string()
        
    def __load_contacts(self):
        with open('./assets/contacts') as json_contacts:
            self.contacts = json.load(json_contacts)
            