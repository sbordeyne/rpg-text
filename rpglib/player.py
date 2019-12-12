from .inventory_system import Inventory
from .entity import Entity
from .utils import parse_dice_format, cast
from .combat_system import Monster
from .quest_system import QuestLog
from .game_timer import Calendar


class Player(Entity):
    def __init__(self, game):
        self.health_rolls = []
        self.mana_rolls = []
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
        self.quest_log = QuestLog(self)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, amount):
        self._health = min(amount, self.max_health)

    @property
    def max_health(self):
        return sum([hr + self.stats.con.modifier for hr in self.health_rolls])

    @max_health.setter
    def max_health(self, value):
        pass

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, amount):
        self._mana = min(amount, self.max_mana)

    @property
    def max_mana(self):
        return sum([mr + self.stats.int.modifier for mr in self.mana_rolls])

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
Location : {str(self.location)} ; Level {self.level} {str(self.job).capitalize()}
STATS : {str(self.stats)}"""

    def melee_attack(self):
        default = ["hands", parse_dice_format("1d4"), []]
        weapon = self.inventory.equipped.r_hand
        if weapon is not None:
            default[0] = self.inventory.equipped.r_hand.display_name
            default[1] = weapon.damage + self.stats.str.modifier
            if weapon.effects_on_hit:
                default[2].extend(weapon.effects_on_hit)
        self.damage = default

    def ranged_attack(self):
        default = ["hands", parse_dice_format("1d4"), []]
        weapon = self.inventory.equipped.r_hand
        ammunition = self.inventory.equipped.l_hand
        if weapon is not None and self.inventory.has_item(weapon.ammunition_type):
            default[0] = weapon.display_name
            default[1] = weapon.damage + self.stats.dex.modifier + ammunition.damage_modifier
            if weapon.effects_on_hit:
                default[2].extend(weapon.effects_on_hit)
            if ammunition.effects_on_hit:
                default[2].extend(ammunition.effects_on_hit)
        elif weapon is not None:
            print(f"{self.name} tried to attack with {weapon.display_name} but did not have enough ammo!")
            self.damage = ("", 0, [])
            return
        elif weapon is None:
            print(f"{self.name} has no ranged weapon equipped")
            self.damage = ("", 0, [])
            return
        self.damage = default

    def attack(self, opponent=None):
        """Performs an attack on $opponent."""
        weapon = self.inventory.equipped.r_hand
        if weapon is None:
            self.melee_attack()
        elif weapon.weapon_type == "ranged":
            self.ranged_attack()
        else:
            self.melee_attack()
        if isinstance(opponent, str):
            opponent = self.game.combat_system.current_opponent.get_opponent_from_str(opponent)
        elif opponent is None:
            opponent = self.game.combat_system.current_opponent.get_random_opponent()
            
        self.game.combat_system.attack(self, opponent)

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

    @property
    def xp_to_next_level(self):
        return self.job.xp_threshold * self.level

    def try_level_up(self):
        if self.experience >= self.xp_to_next_level:
            self.level += 1
            self.health_rolls.append(parse_dice_format(self.job.hp_die))
            self.mana_rolls.append(parse_dice_format(self.job.mp_die))

    def move(self, direction):
        """Moves the player in $direction (n, s, w, e)"""
        location = self.location.try_move_to(direction)
        if location is not None:
            self.location = location
            print(f"Entered {self.location}")

    def gain_experience(self, xp_value):
        self.experience += xp_value * (1 + self.xp_bonus)
        self.try_level_up()

    def end_combat(self, opponent: Monster):
        self.gain_experience(opponent.xp_value)
        treasure = self.game.treasure_system.add_treasure(opponent.treasure)
        print(f"You won versus {str(opponent)} and gained:",
              f"XP : {opponent.xp_value}",
              f"Treasure : {str(treasure)}")
        for effect in self.status_effects:
            effect.remove()
        self.status_effects = []
        self.stats.reset_temp_stats_modifiers()

    def view(self, quest=None):
        """Views the quest log. You can specify a specific $quest to view."""
        pass

    def use(self, item, target=None):
        """Uses usable item $item."""
        if target is None:
            target = self
        self.inventory.use_item(item, target)
        pass

    def inspect(self, thing):
        """Inspects a $thing"""
        pass

    def rest(self, time="8"):
        """Rests for $time hours. Defaults to 8."""
        n_turns = cast(time, int, 8) * Calendar.minutes_per_hour // Calendar.minutes_per_turn
        self.game.timer.tick(n_turns)
        self.mana += parse_dice_format(f'{time * self.level}{self.job.mp_die}')
        self.health += parse_dice_format(f'{time * self.level}{self.job.hp_die}')
        print(f"You rested for {time} hours.")
        pass

    def serialize(self):
        data = {"name": self.name,
                "job": self.job.name,
                "experience": self.experience,
                "health": self._health,
                "mana": self._mana,
                "position": self.position.tuple,
                "status_effects": self.status_effects,
                "inventory": self.inventory.serialize(),
                "stats": self.stats.serialize(),
                "health_rolls" : self.health_rolls,
                "mana_rolls": self.mana_rolls,
                "quest_log": self.quest_log.serialize(),
            }
        return data

    def deserialize(self, data):
        self.name = data["name"]
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
        self.quest_log.deserialize(data["quest_log"])
        return
