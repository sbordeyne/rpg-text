from .inventory_system import Inventory
from .entity import Entity
from .utils import parse_dice_format


class Player(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = None
        self._job = None
        self.experience = 0
        self._health = self.max_health
        self._mana = self.max_mana
        self.location = self.game.map.get_location_from_position((0, 0))
        self.inventory = Inventory()
        self.damage = ("hands", 0, None)
        self.level = 1
        self.health_rolls = []
        self.mana_rolls = []

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, amount):
        self._health = amount

    @property
    def max_health(self):
        return sum(self.health_rolls)

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, amount):
        self._mana = amount

    @property
    def max_mana(self):
        return sum(self.mana_rolls)

    @property
    def position(self):
        return self.location.position

    @property
    def ac(self):
        return 9 - self.inventory.equipped.get_total_ac()

    @property
    def ac_modifier(self):
        return self.stats.dex.modifier

    @property
    def hit_modifier(self):
        return max(self.stats.dex.modifier, self.stats.str.modifier)

    @property
    def xp_bonus(self):
        pstat_value = self.stats[self.job.primary_stat].value
        if pstat_value < 3:
            return -0.3
        elif 3 <= pstat_value < 6:
            return -0.2
        elif 6 <= pstat_value < 9:
            return -0.1
        elif 9 <= pstat_value < 13:
            return 0
        elif 13 <= pstat_value < 16:
            return 0.05
        elif 16 <= pstat_value < 19:
            return 0.1
        else:
            return 0.2

    def __str__(self):
        return \
            f"""Player {self.name} ; {self.health}/{self.max_health} HP ; {self.mana}/{self.max_mana} MP
Location : {str(self.location)} ; Level {self.level} {str(self.job).capitalize()}"""

    def try_level_up(self):
        current_threshold = self.job.xp_threshold * self.level
        if self.experience >= current_threshold:
            self.level += 1
            self.health_rolls.append(parse_dice_format(self.job.hp_die))
            self.mana_rolls.append(parse_dice_format(self.job.mp_die))

    def move(self, direction):
        """Moves the player in $direction (n, s, w, e)"""
        location = self.location.try_move_to(direction)
        if location is not None:
            self.location = location

    def gain_experience(self, xp_value):
        self.experience += xp_value * (1 + self.xp_bonus)
        self.try_level_up()

    def end_combat(self, xp_value):
        self.gain_experience(xp_value)
        for effect in self.status_effects:
            effect.remove()
        self.status_effects = []
        self.stats.reset_temp_stats_modifiers()

    def serialize(self):
        data = {"job": self.job.name,
                "experience": self.experience,
                "health": self._health,
                "mana": self._mana,
                "position": self.position.tuple,
                "status_effects": self.status_effects,
                "inventory": self.inventory.serialize(),
                "stats": self.stats.serialize(),
                "health_rolls" : self.health_rolls,
                "mana_rolls": self.mana_rolls,
                }
        return data

    def deserialize(self, data):
        self.job = data["job"]
        self.experience = data["experience"]
        self._health = data["health"]
        self._mana = data["mana"]
        self.location = self.game.map.get_location_from_position(data["position"])
        self.status_effects = data["status_effects"]
        self.inventory.deserialize(data["inventory"])
        self.stats.deserialize(data["stats"])
        self.health_rolls = data["health_rolls"]
        self.mana_rolls = data["mana_rolls"]
        return
