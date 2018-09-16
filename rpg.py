#!/usr/local/bin/python3.6
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2015
Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2018
"""

import time
import map_
import battle
import character
import gui

app = gui.simpleapp_tk(None)
app.title('Alien Defense')

app.write('''
 _______  ___      ___   _______  __    _                      
|   _   ||   |    |   | |       ||  |  | |                     
|  |_|  ||   |    |   | |    ___||   |_| |                     
|       ||   |    |   | |   |___ |       |                     
|       ||   |___ |   | |    ___||  _    |                     
|   _   ||       ||   | |   |___ | | |   |                     
|__| |__||_______||___| |_______||_|  |__|                     
 ______   _______  _______  _______  __    _  _______  _______ 
|      | |       ||       ||       ||  |  | ||       ||       |
|  _    ||    ___||    ___||    ___||   |_| ||  _____||    ___|
| | |   ||   |___ |   |___ |   |___ |       || |_____ |   |___ 
| |_|   ||    ___||    ___||    ___||  _    ||_____  ||    ___|
|       ||   |___ |   |    |   |___ | | |   | _____| ||   |___ 
|______| |_______||___|    |_______||_|  |__||_______||_______|
''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

def set_mode():
	""" Select the game mode """	
	# This is an error checking version of reading user input
	# Understanding try/except cases is important for
	# verifying user input. See class module on Exception Handling.
	while True:
		try:
			app.write("Please select a side:")
			app.write("	1. Humans")
			app.write("	2. Aliens")
			app.write("")
			app.wait_variable(app.inputVariable)
			mode = app.inputVariable.get()
		
			if mode == 'quit':
				app.quit()
		
			mode = int(mode)
			if mode not in range(1,3):
				raise ValueError
			else:
			 break
	
		except ValueError:
			app.write("You must enter a valid choice")
			app.write("")
	
	return mode

def set_race(mode):
	""" Set the player's race """
	if mode == 2: # Alien Mode
		app.write("Playing as the Alien Invasion Forces.")
		app.write("")
	
		# race selection - evil
		while True:
			try:
				app.write("Please select your race:")
				app.write("	1. Floater")
				app.write("	2. Sectoid")
				app.write("	3. Muton")
				app.write("	4. Ethereal")
				app.write("")
				app.wait_variable(app.inputVariable)
				race = app.inputVariable.get()
			
				if race == 'quit':
					app.quit()
			
				race = int(race)
				if race not in range(1,5):
					raise ValueError
				else:
					break
		
			except ValueError:
				app.write("You must enter a valid choice")
				app.write("")

	else: # Good Mode
		app.write("Playing as the Earth Defence Forces.")
		app.write("")

		# race selection - good
		while True:
			try:
				app.write("Please select your soldier type:")
				app.write("	1. Assault Weapons")
				app.write("	2. Heavy Weapons")
				app.write("	3. Sniper")
				app.write("	4. Support")
				app.write("	5. Psionic")
				app.write("")
				app.wait_variable(app.inputVariable)
				race = app.inputVariable.get()
			
				if race == 'quit':
					app.quit()
				race = int(race)
			
				if race not in range(1,6):
					raise ValueError
				else:
					break
		
			except ValueError:
				app.write("You must enter a valid choice")
				app.write("")
	
	return race

def set_name():
	""" Set the player's name """
	while True:
		try:
			app.write("Please enter your Character Name:")
			app.write("")
			app.wait_variable(app.inputVariable)
			char_name = app.inputVariable.get()

			if char_name == 'quit':
				app.quit()

			if char_name == '':
				raise ValueError
			else:
				break

		except ValueError:
			app.write("")
			app.write("Your name cannot be blank")

	return char_name

def create_player(mode, race, char_name):
	""" Create the player's character """
	# Aliens
	if mode == 2:
		if race == 1:
			player = character.Floater(char_name, app)
		elif race == 2:
			player = character.Sectoid(char_name, app)
		elif race == 3:
			player = character.Muton(char_name, app)
		else:
			player = character.Ethereal(char_name, app)
	# Humans
	else:
		if race == 1:
			player = character.Assault(char_name, app)
		elif race == 2:
			player = character.Heavy(char_name, app)
		elif race == 3:
			player = character.Sniper(char_name, app)
		elif race == 4:
			player = character.Support(char_name, app)
		else:
			player = character.Psionic(char_name, app)
	return player

def set_difficulty():
	""" Set the difficulty of the game """
	while True:
		try:
			app.write("Please select a difficulty level:")
			app.write("	e - Easy")
			app.write("	m - Medium")
			app.write("	h - Hard")
			app.write("	l - Legendary")
			app.write("")
			app.wait_variable(app.inputVariable)
			difficulty = app.inputVariable.get()

			if difficulty == 'quit':
				app.quit()

			if difficulty not in ['e','m','h','l'] or difficulty == '':
				raise ValueError
			else:
				break

		except ValueError:
			app.write("You must enter a valid choice")
			app.write("")

	return difficulty


def quit_game():
	""" Quits the game """
	while True:
		try:
			app.write("Play Again? (y/n)")
			app.write("")
			app.wait_variable(app.inputVariable)
			quit_choice = app.inputVariable.get()

			if quit_choice == 'quit':
				app.quit()

			if quit_choice not in ['y','n'] or quit_choice == '':
				raise ValueError
			else:
				break

		except ValueError:
			app.write("You must enter a valid choice")
			app.write("")

	return quit_choice

def reset_char():
	"""Resets the game"""
	while True:
		try:
			app.write("Reset all progress? (y/n)")
			app.write("")
			app.wait_variable(app.inputVariable)
			quit_choice = app.inputVariable.get()

			if quit_choice == "quit":
				app.quit()
			elif quit_choice not in ['y','n'] or not quit_choice:
				raise ValueError
			else:
				if quit_choice == 'y':
					return True
				else:
					return False

		except ValueError:
			app.write("You must enter a valid choice")
			app.write("")

def print_results():
	app.write("Game Over!")
	app.write("~"*20)
	app.write("No. Battles: {0}".format(str(battles)))
	app.write("No. Wins: {0}".format(wins))
	app.write("No. Kills: {0}".format(kills))
	app.write("Size of party: {}".format(len(players)))
	app.write("Success Rate (%): {0:.2f}%".format(float(wins*100/battles)))
	app.write("Avg. kills per battle: {0:.2f}".format(float(kills)/battles))
	app.write("")

def startup():
	players = []
	mode = set_mode()
	race = set_race(mode)
	
	while True:
		char_name = set_name()
		race = set_race(mode)
		players.append(create_player(mode, race, char_name))
		for player in players:
			app.write(player)
		app.write("")
		if len(players) > 4:
			app.write("Party is full!")
			break
		else:
			app.write("Create another Character? (y/n)")
			app.wait_variable(app.inputVariable)
			ans = app.inputVariable.get()
			if ans == 'n':
				break

	difficulty = set_difficulty()


battles = 0
wins = 0
kills = 0

players = []
mode = set_mode()

while True:
	char_name = set_name()
	race = set_race(mode)
	players.append(create_player(mode, race, char_name))
	for player in players:
		app.write(player)
	app.write("")
	if len(players) <= 2:
		app.write("Create another Character? (y/n)")
		app.write("")
		app.wait_variable(app.inputVariable)
		ans = app.inputVariable.get()
		if ans == 'n':
			break
	else:
		app.write("Party is full!")
		app.write("")
		time.sleep(1)
		break
		
difficulty = set_difficulty()

while True:
	move = map_.Map(players, 32, mode, difficulty, app)
	while True:
		enemies, leave = move.run()
		if leave:
			break
		encounter = battle.Battle(players, enemies, app)
		battle_wins, battle_kills, loss = encounter.play()
		battles += 1
		wins += battle_wins
		kills += battle_kills
		if loss:
			break

	print_results()
		
	quit = quit_game()

	if quit == "n":
		app.write("Thank you for playing Alien Defense.")
		time.sleep(2)
		app.quit()

	else:
		# Playing again - reset all enemies and players
		reset = reset_char()
		if reset:
			startup()
		else:
			for player in players:
				player.reset()
			for enemy in enemies:
				enemy.reset()
