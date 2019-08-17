class Constants:
	def __init__(self):
		self.directions = {"N":"north", "S":"south", "W":"west", "E":"east"}

class Game():
	"""
		Main game class, handles the global behavior of the game.
	"""
	def __init__(self):
		self.done = False
		self.CONST = Constants()
		self.load_game()
	def load_game(self):
		try:
			save = open("save.dat", "r")
			self.data = save.readlines()
		except IOError:
			self.new_game()
		finally:
			save.close()
	def new_game(self):
		pass
	def save_game(self):
		with open("save.dat", "w") as save:
			for d in self.data:
				save.write(d)
	def mainloop(self):
		while not self.done:
			pass
		self.save_game()
		pass
