from .utils import sanitized_input, parse_dice_format
import random
import json
from .entity import Entity


class Monster(Entity):
    def __init__(self, name):
        super().__init__()
        with open("data/monsters.json") as f:
            data = json.load(f).get(name, {})
        self.name = name

        self.level = data.get("level", 1)
        self.max_health = sum([random.randint(1, 8) for i in range(self.level)])
        self.health = self.max_health
        self.ac = data.get("ac", 9)
        self.attacks = data.get("attacks", {"normal": "1d6"})
        self.ac_modifier = data.get("ac_modifier", 0)
        self.hit_modifier = data.get("hit_modifier", 0)
        self.xp_value = data.get("xp_value", 50)

    @property
    def damage(self):
        attack = random.choice(self.attacks.keys())
        attack_data = self.attacks[attack]
        if isinstance(attack_data, str):
            return attack, parse_dice_format(attack_data), None
        elif isinstance(attack_data, list):
            return attack, parse_dice_format(attack_data[0]), attack_data[1:]


class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.n_turns = 0
        self.fleeing = False

    def start_combat(self, opponent):
        self.n_turns = 0
        if isinstance(opponent, str):
            opponent = Monster(opponent)
        elif not isinstance(opponent, Monster):
            raise TypeError

        while not self.is_combat_finished(opponent):
            self.n_turns += 1
            command = sanitized_input("> ", error_msg="Invalid Command!")
            print(self.combat_state(opponent))
            while not self.game.command_system.parse_combat(command):
                print("Invalid command. Type 'help' for help.")
                command = sanitized_input("> ", error_msg="Invalid Command!")
            opponent.apply_status_effects()
            self.game.player.apply_status_effects()

        self.finish_combat(opponent)

    def is_combat_finished(self, opponent):
        return opponent.is_dead or self.game.player.is_dead or self.fleeing

    def combat_state(self, opponent):
        player = self.game.player
        opponent_status = f"{opponent.name} : {opponent.health}/{opponent.max_health} HP"
        player_status = f"{player.name} : {player.health}/{player.max_health} HP {player.mana}/{player.max_mana} MP"
        player_moves = " ".join([c.command for c in self.game.command_system.combat_commands])
        return "\n".join([opponent_status, player_status, player_moves])

    def finish_combat(self, opponent):
        if self.game.player.is_dead:
            self.game.game_over()
        else:
            self.game.player.gain_experience(opponent.xp_value)
            self.game.map.remove_opponent(opponent)

    @classmethod
    def get_hit(cls, attacker, defender):
        diff_lvl = defender.level - attacker.level
        def_ac = (20 - defender.ac) + diff_lvl + defender.ac_modifier
        rng = random.randint(1, 20) + attacker.hit_modifier
        return rng >= def_ac

    @classmethod
    def attack(cls, attacker, defender):
        if CombatSystem.get_hit(attacker, defender):
            attack, damage, status_effects = attacker.damage
            defender.take_damage(damage)
            if status_effects is None:
                print(f"{attacker.name} attacked {defender.name} with {attack} and hit for {damage}!")
            else:
                defender.inflict_status_effects(*status_effects)
                print(f"{attacker.name} attacked {defender.name} with {attack} and hit for {damage}"
                      f"({', '.join(status_effects)})!")
        else:
            print(f"{attacker.name} attacked {defender.name} with {attack} and did not hit!")