class Entity():
	def __init__(self):
		self.health = 0

		pass
	def take_damage(self):
		pass

class Character(Entity):
	def __init__(self):
		super().__init__(self)
