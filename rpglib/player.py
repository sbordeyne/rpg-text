from .inventory_system import Inventory
from .entity import Entity
from .utils import parse_dice_format
from .combat_system import Monster


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

    def melee_attack(self):
        default = ["hands", parse_dice_format("1d4"), []]
        weapon = self.inventory.equipped.r_hand
        if weapon is not None:
            default[0] = self.inventory.equipped.r_hand.name
            default[1] = parse_dice_format(weapon.damage) + self.stats.str.modifier
        if weapon.effects_on_hit:
            default[2].extend(weapon.effects_on_hit)
        self.damage = default

    def ranged_attack(self):
        default = ["hands", parse_dice_format("1d4"), []]
        weapon = self.inventory.equipped.r_hand
        ammunition = self.inventory.equipped.l_hand
        if weapon is not None and self.inventory.has_item(weapon.ammunition_type):
            default[0] = weapon.name
            default[1] = parse_dice_format(weapon.damage) + self.stats.dex.modifier + ammunition.damage_modifier
        elif weapon is not None:
            print(f"{self.name} tried to attack with {weapon.name} but did not have enough ammo!")
            self.damage = ("", 0, [])
            return
        elif weapon is None:
            print(f"{self.name} has no ranged weapon equipped")
            self.damage = ("", 0, [])
            return
        if weapon.effects_on_hit:
            default[2].extend(weapon.effects_on_hit)
        if ammunition.effects_on_hit:
            default[2].extend(ammunition.effects_on_hit)
        self.damage = default

    def attack(self):
        """Performs an attack."""
        weapon = self.inventory.equipped.r_hand
        if weapon is None:
            self.melee_attack()
        elif weapon.weapon_type == "ranged":
            self.ranged_attack()
        else:
            self.melee_attack()

    def flee(self):
        """Attempts to flee the fight."""
        diff_level = self.game.combat_system.current_opponent.level - self.level
        if diff_level > 5:
            self.game.combat_system.fleeing = True
            print("You fled the fight!")
        elif -5 < diff_level < 5:
            roll = parse_dice_format('1d10')
            if roll >= (diff_level + 5):
                self.game.combat_system.fleeing = True
                print("You fled the fight!")
            else:
                print("You failed to flee the fight!")
        else:
            print("You cannot flee the fight!")
        pass

    def cast(self, spell, target=None):
        """Casts $spell on $target. $target optional."""
        if target is None or target in ("self", "player"):
            target = self
        else:
            target = Monster(target)
        self.spell_list.cast(spell, target)
        pass

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
