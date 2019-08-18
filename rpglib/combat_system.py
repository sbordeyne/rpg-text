from .utils import sanitized_input
import random
import json


class Monster:
    def __init__(self, name):
        with open("data/monsters.json") as f:
            data = json.load(f).get(name, {})

        self.level = data.get("level", 1)
        self.max_health = sum([random.randint(1, 8) for i in range(self.level)])
        self.health = self.max_health
        self.ac = data.get("ac", 9)
        self.attacks = data.get("attack", list(range(1, 7)))
        self.ac_modifier = data.get("ac_modifier", 0)
        self.hit_modifier = data.get("hit_modifier", 0)

    @property
    def damage(self):
        return random.choice(self.attacks)

    def take_damage(self, amount):
        self.health -= amount


class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.n_turns = 0

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
        self.finish_combat(opponent)

    def is_combat_finished(self, opponent):
        return opponent.is_dead or self.game.player.is_dead

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
            damage = attacker.damage
            defender.take_damage(damage)
            print(f"{attacker.name} attacked {defender.name} and hit for {damage}!")
        else:
            print(f"{attacker.name} attacked {defender.name} and did not hit!")