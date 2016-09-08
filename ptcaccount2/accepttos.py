#!/usr/bin/python
# -*- coding: utf-8 -*-

"""accept-tos.py: Example script to accept in-game Terms of Service"""

from pgoapi import PGoApi
from pgoapi.utilities import f2i
from pgoapi import utilities as util
from pgoapi.exceptions import AuthException, ServerSideRequestThrottlingException, NotLoggedInException
import pprint
import time
import threading
import random
import string
import os

#borrowed from https://github.com/gabrielsoldani/Gastly
class Pokedex:
  Bulbasaur = 1
  Charmander = 4
  Squirtle = 7

STARTER_POKEMON = (Pokedex.Bulbasaur, Pokedex.Charmander, Pokedex.Squirtle)
#end of borrowing

def accept_tos(username, password, location, proxy):
    try:
        accept_tos_helper(username, password, location, proxy)
    except ServerSideRequestThrottlingException as e:
        print('Server side throttling, Waiting 10 seconds.')
        time.sleep(10)
        accept_tos_helper(username, password, location, proxy)
    except NotLoggedInException as e1:
        print('Could not login, Waiting for 10 seconds')
        time.sleep(10)
        accept_tos_helper(username, password, location, proxy)

def accept_tos_helper(username, password, location, proxy):
    print "Trying to accept Terms of Service for {}.".format(username)
    failMessage = "Maybe the HTTPS proxy is not working? {} did not accept Terms of Service.".format(username)

    api = PGoApi()
    if proxy != None:
        api.set_proxy({"http":proxy})

    location = location.replace(" ", "")
    location = location.split(",")
    api.set_position(43.6427431,-79.3762986, 21)
    #api.set_position(float(location[0]), float(location[1]), 0.0)
    api.set_authentication(provider = 'ptc', username = username, password = password)
    response = api.app_simulation_login()
    if response == None:
        print "Servers do not respond to login attempt. " + failMessage
        return

    time.sleep(1)
    req = api.create_request()
    req.mark_tutorial_complete(tutorials_completed = 0, send_marketing_emails = False, send_push_notifications = False)
    response = req.call()
    if response == None:
        print "Servers do not respond to accepting the ToS. " + failMessage
        return

    print('Accepted Terms of Service for {}'.format(username))
    time.sleep(2)
    req.claim_codename(codename = username)
    response = req.call()
    print('Claimed username: {}'.format(username))
    time.sleep(2)
    
    #choose a pokemon
    
    chosenpokemon = random.choice(STARTER_POKEMON)
    req.encounter_tutorial_complete(pokemon_id=chosenpokemon)
    response = req.call()
    print('Chose {} as starter pokemon'.format(chosenpokemon))
 
    if response['status_code'] == 3:
        print('The following account is banned! {}'.format(username))
        if os.path.exists("banned.txt"):
            f = open('./banned.txt', 'a+b')
        else:
            f = open('./banned.txt', 'w+b')
            f = open('./banned.txt', 'w+b')
        f.write("%s\n" % (username))
        f.close()
    else:
        print('Not banned...')
