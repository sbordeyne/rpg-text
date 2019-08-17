import random as rd
from copy import deepcopy as copy

class Constants:
	def __init__(self):
		self.directions = {"N":"north", "S":"south", "W":"west", "E":"east"}

class Inventory(list):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		pass

class Character():
	def __init__(self, name):
		self.name = name
		self.xp = 0
		self.xp_to_level = 1500
		self.level = 1
		self.inventory = Inventory()
	def add_xp(self, xp_to_add):
		self.xp += xp_to_add
		if self.xp >= self.xp_to_level:
			self.xp_to_level *= 2
			self.level += 1

def get_available_directions(previous=None):
	if previous is None:
		return ["N", "S", "E", "W"]
	else:
		previous = {"N":"S", "S":"N", "W":"E", "E":"W"}[previous] #get the opposite, if you come from north, you can go south, and vice-versa
		n = rd.randint(0, 3)
		dirs = list(CONST.directions.keys())
		dirs.pop(dirs.index(previous.upper()))
		rd.shuffle(dirs)
		dirs = copy(dirs[:n])
		dirs.append(previous)
		return dirs

done = False
name = input("What's your character name ?\t")
character = Character(name)
CONST = Constants()
direction = None
round_number = 1
previous_round_number = 0
while not done:
	if round_number > previous_round_number:
		previous_round_number = round_number
		available_directions = get_available_directions(direction)
	print("You arrive at a crossroad.")
	if len(available_directions)>1:
		print("You can go {} and {}.".format(", ".join(available_directions[:-1]), available_directions[-1]))
	else:
		print("You can only go {}.".format(available_directions[0]))
	direction = input("Where do you want to go ?\t").upper()
	if direction in ["N", "S", "E", "W"]:
		if direction in available_directions:
			print("You went {}".format(CONST.directions[direction]))
			round_number += 1
		elif direction not in available_directions:
			print("You can't go there !")
			continue
	else:
		if direction == "EXIT":
			done = True
		else:
			print("Direction not recognized")
			continue
