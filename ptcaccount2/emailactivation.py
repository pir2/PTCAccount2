import requests
import io
import time
import os
import json
import urllib2
import re

def ActivateEmail(username):
  #Personal inbucket.org email server
  url = "http://inbucket.org//api/v1/mailbox/"+username
  
  #Create request to grab mailbox
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  mailbox = json.loads(f.read())
  count = 0
  
  #check to see if email has arrived for next 3600 seconds
  #grab the emailid if email has arrived
  while not mailbox and count < 360:
  	req = urllib2.Request(url)
  	f = opener.open(req)
  	mailbox = json.loads(f.read())
  	count+=1
  	time.sleep(1)
  	print 'Checked email ' + count + ' time(s)'
  
  #assign the emailid
  emailid = mailbox[0]["id"]
  
  #get the email content
  emailURL = url + "/" + emailid + "/source"
  emailreq = urllib2.Request(emailURL)
  emailopen = opener.open(emailreq)
  emailcontent = emailopen.read()
  
  #search for activation link
  ActURL = re.findall('https://club.pokemon.com/us/pokemon-trainer-club/activated/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', emailcontent)
  
  #open activation link
  actreq = urllib2.Request(ActURL[0])
  actopen = opener.open(actreq)
  actcontent = actopen.read()
  
  #check to make sure email is avlidated
  if 'Thank you for signing up! Your account is now active.' in actcontent:
  	print 'Email Validated'
  else:
    print 'Could not validate email'
