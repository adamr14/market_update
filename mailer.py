#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:20:15 2019

@author: adamrankin
"""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from datetime import date

class Mailer():
    
    def __init__(self):
        self.port = 465
        self.context = ssl.create_default_context()
        self.__load_contacts()
        #Used for testing
        #self.contacts = {"adamr14@vt.edu": "Adam"}
        self.__load_password()
        self.body_html=''
        self.body_text=''
        self.message = MIMEMultipart("alternative")
        
    
    
    def send_email(self):
        self.message["Subject"] = "Daily Market Update for " + date.today().strftime("%m/%d/%Y")
        self.message["From"] = "dailymarketjournal@gmail.com"
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login("dailymarketjournal@gmail.com", self.password)
            for receiver in self.contacts.keys():
                self.message["To"] = receiver
                #
                # builds email as text
                #
                content_text='Hey ' + self.contacts[receiver] +',\n\n'
                content_text+='Here is your daily market update:\n\n\n'
                content_text+=self.body_text
                content_text+='\n\nAll data collected from Yahoo Finance and the Fed Website\n\nDirect questions and Suggestions to Adam Rankin'
                
                #
                # builds email in html
                #
                content_html="""\
                <html>
                    <body>
                        <p style="color:black;">Hey """ + self.contacts[receiver] +""", <br><br>
                        Here are today's closing market numbers:</p>"""
                content_html+=self.body_html
                content_html+="""\
                        <p style="color:black;"><br><br>All data collected from Yahoo Finance and the Federal Reserve Website</p>
                    </body>
                </html>
                """
                part1 = MIMEText(content_text, "plain")
                part2 = MIMEText(content_html, "html")
                self.message.attach(part1)
                self.message.attach(part2)
                server.sendmail("dailymarketjournal@gmail.com", receiver, self.message.as_string())
                
    def add_dataframe_to_body(self, title, table, url):
        self.body_html+='<h2 style="color:black;"><a href=' + url + '>'+title+'</a></h2>'
        self.body_html+=table.to_html()
        self.body_text+= title + '\n'
        self.body_text+=table.to_string()
        
    def add_image_to_body(self, img):
        with open('./attachments/' + img, 'rb') as f:
            mime = MIMEBase('image', 'png', filename=img)
            # add required header data:
            mime.add_header('Content-Disposition', 'attachment', filename=img)
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
            # read attachment file content into the MIMEBase object
            mime.set_payload(f.read())
            # encode with base64
            encoders.encode_base64(mime)
            # add MIMEBase object to MIMEMultipart object
            self.message.attach(mime)
            self.body_html+='<p><img src="cid:0" alt="UST Yield Curve" style="width:900px;height:300px;"></p>'
        
    def __load_contacts(self):
        with open('./assets/contacts') as json_contacts:
            self.contacts = json.load(json_contacts)
        
    def __load_password(self):
        with open('./assets/key') as json_key:
            self.password = json.load(json_key)['password']
