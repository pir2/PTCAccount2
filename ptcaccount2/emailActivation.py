import requests
import io
#from tempmail import TempMail #pip install temp-mail
from bs4 import BeautifulSoup
import time
import os
import json
import urllib2
import re

def ActivateEmail(username)
  url = "http://inbucket.org//api/v1/mailbox/"+username
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  json = json.loads(f.read())
  emailid = json[0]["id"]
  
  
  emailURL = url + "/" + emailid + "/source"
  emailreq = urllib2.Request(emailURL)
  emailopen = opener.open(emailreq)
  emailcontent = emailopen.read()
  
  ActURL = re.findall('https://club.pokemon.com/us/pokemon-trainer-club/activated/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', emailcontent)
  
  actreq = urllib2.Request(ActURL[0])
  actopen = opener.open(actreq)
  actcontent = actopen.read()
  
  if 'Thank you for signing up! Your account is now active.' in actcontent:
  	print 'Email Validated'
