#!/usr/bin/python
# -*- coding: utf-8 -*-

"""accept-tos.py: Example script to accept in-game Terms of Service"""

from pgoapi import PGoApi
from pgoapi.utilities import f2i
from pgoapi import utilities as util
from pgoapi.exceptions import AuthException
import pprint
import time
import threading
import random

#borrowed from https://github.com/gabrielsoldani/Gastly
class Pokedex:
  Bulbasaur = 1
  Charmander = 4
  Squirtle = 7

STARTER_POKEMON = (Pokedex.Bulbasaur, Pokedex.Charmander, Pokedex.Squirtle)
#end of borrowing

def accept_tos(username, password):
	api = PGoApi()
	api.set_position(43.6427431,-79.3762986, 21)
	api.login('ptc', username, password)
	time.sleep(2)
	req = api.create_request()
	req.mark_tutorial_complete(tutorials_completed = 0, send_marketing_emails = False, send_push_notifications = False)
	response = req.call()
	print('Accepted Terms of Service for {}'.format(username))
	req.claim_codename(codename = username)
	response = req.call()
	print('Claimed username: {}'.format(username))
        time.sleep(2)
        req.encounter_tutorial_complete(pokemon_id=chosenpokemon)
        response = req.call()
        print('Chose {} as starter pokemon'.format(chosenpokemon))
 
	#print('Response dictionary: \r\n{}'.format(pprint.PrettyPrinter(indent=4).pformat(response)))

#accept_tos('username', 'password')
