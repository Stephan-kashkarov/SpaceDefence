#!/usr/local/bin/python3.6
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2015
Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2018
"""

# import required Python modules
import time
import random
import item

######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character:
	""" Defines the attributes and methods of the base Character class """
	
	def __init__(self, char_name, app):
		""" Parent constructor - called before child constructors """
		self.attack_mod = 1.0
		self.defense_mod = 1.0
		self.name = char_name
		self.shield = 0
		self.max_shield = 50
		self.inventory = []
		self.app = app
		self.battleX = 0
		self.battleY = 0
		self.money = 10

	def __str__(self):
		""" string representation of character """
		return str("You are " + self.name + " the " + self.__class__.__name__)

	def move(self, player):
		"""
		Defines any actions that will be attempted before individual
		character AI kicks in - applies to all children
		"""
		move_complete = False
		if self.health < 50 and self.medikits > 0:
			self.set_stance('d')
			self.use_medikit()
			move_complete = True
		return move_complete

#### Character Attacking Actions ####

	def set_stance(self, stance_choice):
		""" sets the fighting stance based on given parameter """
		
		if stance_choice == "a":
			self.attack_mod = 1.3
			self.defense_mod = 0.6
			self.app.write(self.name + " chose aggressive stance.")

		elif stance_choice == "d":
			self.attack_mod = 0.6
			self.defense_mod = 1.3
			self.app.write(self.name + " chose defensive stance.")

		else:
			self.attack_mod = 1.0
			self.defense_mod = 1.0
			self.app.write(self.name + " chose balanced stance.")
		self.app.write("")

	def attack_enemy(self, target, modifier):
		''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
		to be targeted). Returns True if target killed, False if still alive.'''

		roll = random.randint(5,20)
		hit = int(roll * self.attack_mod * self.attack * float(modifier/100))
		self.app.write(self.name + " attacks " + target.name + ".")
		self.app.write("-"*20)
		self.app.write("Attack = roll * attack_mod * base attack * cover")
		self.app.write("  {}   =  {}  *    {}      *     {}      * {:2f}".format(
			hit,
			roll,
			self.attack_mod,
			self.attack,
			(modifier/100),
			))
		time.sleep(1)

		crit_roll = random.randint(1, 10)
		if crit_roll == 10:
			hit = hit*2
			self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
			time.sleep(1)

		kill = target.defend_attack(hit)
		time.sleep(1)

		if kill:
			self.app.write(self.name + " has killed " + target.name + ".")
			self.app.write("")
			time.sleep(1)
			return True
		else:
			return False

	def defend_attack(self, att_damage):
		''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
		a parameter. Returns True is character dies, False if still alive.'''
		
		# defend roll
		roll = random.randint(1, 5)
		block = int(roll * self.defense_mod * self.defense)
				
		# Roll for dodge - must roll a 10 (1% chance)
		dodge_roll = random.randint(1, 100)
		if dodge_roll == 10:
			self.app.write(self.name + " successfully dodges the attack!")
			block = att_damage
			time.sleep(1)

		# Calculate damage from attack
		damage = att_damage - block
		if damage < 0:
			damage = 0

		# If character has a shield, shield is depleted, not health
		if self.shield > 0:
			# Shield absorbs all damage if shield is greater than damage
			if damage <= self.shield:
				self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
				time.sleep(1)
				self.shield = self.shield - damage
				damage = 0
			# Otherwise some damage will be sustained and shield will be depleted
			elif damage != 0:
				self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
				time.sleep(1)
				damage = damage - self.shield
				self.shield = 0
			
		# Reduce health
		self.app.write("Block = roll * defense_mod * defense")
		self.app.write(" {}   = {}   *     {}      *   {}".format(block, roll, self.defense_mod, self.defense))
		self.app.write("Damage = Attack - Block")
		self.app.write("  {}   =   {}   -  {}".format(damage, att_damage, block))
		self.app.write("-"*20)
		self.app.write(self.name + " suffers " + str(damage) + " damage!")
		self.health = self.health - damage
		time.sleep(1)
			
		# Check to see if dead or not
		if self.health <= 0:
			self.health = 0
			self.app.write(self.name + " is dead!")
			self.app.write("")
			time.sleep(1)
			return True
		else:
			self.app.write(self.name + " has " + str(self.health) + " hit points left")
			self.app.write("")
			time.sleep(1)
			return False

#### Character Ability Actions ####

	def valid_ability(self, choice):
		''' Checks to see if the ability being used is a valid ability i.e. can be used by
		that race and the character has enough adrenaline '''

		valid = False

		# Determine this character's race
		# This is a built-in property we can use to work out the
		# class name of the object (i.e. their race)
		race = self.__class__.__name__
		
		if choice == 1:
			if race in ["Ethereal","Psionic"] and self.adrenaline >= 10:
				valid = True
		elif choice == 2 and self.adrenaline >= 20:
			valid = True
				
		return valid

	def use_ability(self, choice, target=False):
		''' Uses the ability chosen by the character. Requires 2 parameters - the ability
		being used and the target of the ability (if applicable). '''

		kill = False

		if choice == 1:
			kill = self.throw(target)
		elif choice == 2:
			self.engage_shield()
		else:
			self.app.write("Invalid ability choice. Ability failed!")
			self.app.write("")

		return kill

	def throw(self, target):
		self.adrenaline -= 10
		self.app.write(self.name + " throws " + target.name + " through the air!")
		time.sleep(1)
			
		roll = random.randint(1, 10)
		defense_roll = random.randint(1, 10)
		damage = int(roll * self.mind) - int(defense_roll * target.resistance)
		if damage < 0:
			damage = 0
			
		if target.shield > 0:
			if damage <= target.shield:
				self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
				time.sleep(1)
				target.shield = target.shield - damage
				damage = 0
			elif damage != 0:
				self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
				time.sleep(1)
				damage = damage - target.shield
				target.shield = 0
												
		self.app.write(target.name + " takes " + str(damage) + " damage.")
		self.app.write("")
		time.sleep(1)
		target.health = target.health - damage
			
		if target.health <= 0:
			target.health = 0
			self.app.write(target.name + " is dead!")
			self.app.write("")
			time.sleep(1)
			return True

		else:
			self.app.write(target.name + " has " + str(target.health) + " hit points left")
			self.app.write("")
			time.sleep(1)
			return False

	def engage_shield(self):
		self.adrenaline -= 20
		self.app.write(self.name + " engages a personal shield!")
		time.sleep(1)
		if self.shield <= self.max_shield:
			self.shield = self.max_shield
		self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
		self.app.write("")
		time.sleep(1)

#### Character Item Actions ####

	def use_medikit(self):
		"""
		Uses a medikit if the player has one. Returns True if has medikit,
		false if hasn't
		"""
		if self.medikits >= 1:
			self.medikits -= 1
			self.health += 250
			if self.health > self.max_health:
				self.health = self.max_health
			self.app.write(self.name + " uses a medikit!")
			time.sleep(1)
			self.app.write(self.name + " has " + str(self.health) + " hit points.")
			self.app.write("")
			time.sleep(1)
			return True
		else:
			self.app.write("You have no medikits left!")
			self.app.write("")
			return False

#### Miscellaneous Character Actions ####

	def reset(self):
		''' Resets the character to its initial state '''
		
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits
		self.shield = 0
		
	def print_status(self):
		''' Prints the current status of the character '''
		self.app.write(self.name + "'s Status:")

		
		health_bar = "Health: "
		health_bar += "|"
		i = 0
		while i <= self.max_health:
			if i <= self.health:
				health_bar += "#"
			else:
				health_bar += " "
			i += 25
		health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
		self.app.write(health_bar)
				
		if self.max_adrenaline > 0:
			adrenaline_bar = "Adrenaline: "
			adrenaline_bar += "|"
			i = 0
			while i <= self.max_adrenaline:
				if i <= self.adrenaline:
					adrenaline_bar += "*"
				else:
					adrenaline_bar += " "
				i += 10
			adrenaline_bar += "| " + str(self.adrenaline) + " ap (" + str(int(self.adrenaline*100/self.max_adrenaline)) +"%)"
			self.app.write(adrenaline_bar)

	 
		if self.shield > 0:
			shield_bar = "Shield: "
			shield_bar += "|"
			i = 0
			while i <= 100:
				if i <= self.shield:
					shield_bar += "o"
				else:
					shield_bar += " "
				i += 10
			shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
			self.app.write(shield_bar)
   

		self.app.write("Medikits remaining: " + str(self.medikits))
		self.app.write("")

######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Assault(Character):
	'''Defines the attributes of an Assault Weapons Soldier in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Assault class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 50
		self.max_adrenaline = 40
		self.starting_medikits = 1
		self.attack = 7
		self.defense = 8
		self.mind = 5
		self.resistance = 4
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Assault class """
		move_complete = Character.move(self, player)
		if not move_complete:
			if self.health*100 / self.max_health > 75:
				self.set_stance('a')
			elif self.health*100 / self.max_health > 30:
				self.set_stance('b')
			else:
				self.set_stance('d')
			if self.shield == 0 and self.adrenaline >= 20:
				self.use_ability(2)
			else:
				return self.attack_enemy(player, modifier)
		return False

class Heavy(Character):
	'''Defines the attributes of a Heavy Weapons Soldier in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Heavy class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 75
		self.max_adrenaline = 30
		self.starting_medikits = 1
		self.attack = 9
		self.defense = 6
		self.mind = 4
		self.resistance = 5
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Heavy class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('a')
			return self.attack_enemy(player, modifier)
		return False
		
class Sniper(Character):
	'''Defines the attributes of a Sniper in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Sniper class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 50
		self.max_adrenaline = 60
		self.starting_medikits = 1
		self.attack = 6
		self.defense = 8
		self.mind = 8
		self.resistance = 8
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Sniper class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('d')
			if self.shield == 0 and self.adrenaline >= 20:
				self.use_ability(2)
			else:
				return self.attack_enemy(player, modifier)
		return False

class Support(Character):
	'''Defines the attributes of a Support Soldier in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Support class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 75
		self.max_adrenaline = 40
		self.starting_medikits = 2
		self.attack = 3
		self.defense = 9
		self.mind = 6
		self.resistance = 10
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Support class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('d')
			# Support soldiers shield if they don't have one
			if self.shield == 0 and self.adrenaline >= 20:
				self.use_ability(2)
			else:
				return self.attack_enemy(player, modifier)
		return False

class Floater(Character):
	'''Defines the attributes of a Floater in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Floater class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 45
		self.max_adrenaline = 20
		self.starting_medikits = 0
		self.attack = 3
		self.defense = 3
		self.mind = 0
		self.resistance = 0
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Floater class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('d')
			return self.attack_enemy(player, modifier)
		return False

class Sectoid(Character):
	'''Defines the attributes of a Sectoid in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Sectoid class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 65
		self.max_adrenaline = 35
		self.starting_medikits = 0
		self.attack = 7
		self.defense = 5
		self.mind = 2
		self.resistance = 4
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Sectoid class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('b')
			return self.attack_enemy(player, modifier)
		return False

class Muton(Character):
	'''Defines the attributes of a Muton in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Muton class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 85
		self.max_adrenaline = 20
		self.starting_medikits = 1
		self.attack = 9
		self.defense = 7
		self.mind = 4
		self.resistance = 6
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Muton class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('a')
			return self.attack_enemy(player, modifier)
		return False

class Ethereal(Character):
	'''Defines the attributes of an Ethereal in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Ethereal class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 50
		self.max_adrenaline = 100
		self.starting_medikits = 2
		self.attack = 5
		self.defense = 6
		self.mind = 10
		self.resistance = 10
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Ethereal class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('b')
			if self.adrenaline >= 10:
				return self.use_ability(1, player)
			else:
				return self.attack_enemy(player, modifier)
		return False

class Psionic(Character):
	'''Defines the attributes of a Psionic Soldier in the game. Inherits the constructor and methods
	of the Character class '''
	
	# Constructor for Psionic class
	def __init__(self, char_name, app):
		Character.__init__(self, char_name, app)
		self.max_health = 55
		self.max_adrenaline = 100
		self.starting_medikits = 2
		self.attack = 5
		self.defense = 6
		self.mind = 10
		self.resistance = 10
		self.health = self.max_health
		self.adrenaline = self.max_adrenaline
		self.medikits = self.starting_medikits

	def move(self, player, modifier):
		""" Defines the AI for the Psionic class """
		move_complete = Character.move(self, player)
		if not move_complete:
			self.set_stance('d')
			if self.shield == 0 and self.adrenaline >= 20:
				self.use_ability(2)
			elif self.adrenaline >= 10:
				return self.use_ability(1, player)
			else:
				return self.attack_enemy(player, modifier)
		return False
