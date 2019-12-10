from .utils import sanitized_input, parse_dice_format
import random
import json
from .entity import Entity


class MonsterParty:
    def __init__(self, party_name):
        super().__init__()
        self.monsters = {}
        self.name = party_name
        if party_name.startswith('party'):
            self._init_party()
        else:
            self._init_single_party()
    
    def _init_party(self):
        with open('data/monster_parties.json') as f:
            data = json.load(f).get(self.name, {})
        table = data.get('monsters', {})
        for monster_name in table.keys():
            n_mobs = parse_dice_format(table[monster_name])
            for i in range(n_mobs):
                self.monsters[monster_name + str(i + 1)] = Monster(monster_name)
        self.treasure = data.get("treasure", None)
    
    def _init_single_party(self):
        self.monsters[self.name] = Monster(self.name)
        self.treasure = self.monsters[self.name].treasure
    
    def take_combat_turn(self, player):
        for monster in self.monsters:
            self.monsters[monster].take_combat_turn(player)
    
    @property
    def is_dead(self):
        rv = True
        for mob in self.monsters.values():
            if not mob.is_dead:
                rv = False
        return rv


class Monster(Entity):
    def __init__(self, name):
        super().__init__()
        with open("data/monsters.json") as f:
            data = json.load(f).get(name, {})
        self.name = name
        self.type_name = 'monster'

        self.level = data.get("level", 1)
        self.lifedice = data.get("lifedice", f"{self.level}d8")
        self.max_health = parse_dice_format(self.lifedice)
        self.health = self.max_health
        self.ac = data.get("ac", 9)
        self.attacks = data.get("attacks", {"normal": "1d6"})
        self.ac_modifier = data.get("ac_modifier", 0)
        self.hit_modifier = data.get("hit_modifier", 0)
        self.xp_value = data.get("xp_value", 50)
        self.job = data.get("job", "warrior")
        self.treasure = data.get("treasure", None)
        self.monster_type = data.get("monster_type", None)

    @property
    def damage(self):
        attack = random.choice(self.attacks.keys())
        attack_data = self.attacks[attack]
        if isinstance(attack_data, str):
            return attack, parse_dice_format(attack_data), None
        elif isinstance(attack_data, list):
            return attack, parse_dice_format(attack_data[0]), attack_data[1:]
    
    def take_combat_turn(self, player):
        CombatSystem.attack(self, player)


class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.n_turns = 0
        self.fleeing = False
        self.current_opponent = None
        self.in_combat = False

    def start_combat(self, opponent):
        self.n_turns = 0
        self.in_combat = True
        if isinstance(opponent, str):
            opponent = MonsterParty(opponent)
        elif not isinstance(opponent, (Monster, MonsterParty)):
            raise TypeError

        self.current_opponent = opponent

        while not self.is_combat_finished():
            self.n_turns += 1
            command = sanitized_input("> ", error_msg="Invalid Command!")
            print(self.combat_state())
            while not self.game.command_system.parse(command, self.game.command_system.combat_commands):
                print("Invalid command. Type 'help' for help.")
                command = sanitized_input("> ", error_msg="Invalid Command!")
            opponent.apply_status_effects()
            self.game.player.apply_status_effects()
            opponent.take_combat_turn(self.game.player)

        self.finish_combat()

    def is_combat_finished(self):
        return self.current_opponent.is_dead or self.game.player.is_dead or self.fleeing

    def combat_state(self):
        opponent = self.current_opponent
        player = self.game.player
        opponent_status = f"{opponent.name} : {opponent.health}/{opponent.max_health} HP"
        player_status = f"{player.name} : {player.health}/{player.max_health} HP {player.mana}/{player.max_mana} MP"
        player_moves = " ".join([c.command for c in self.game.command_system.combat_commands])
        return "\n".join([opponent_status, player_status, player_moves])

    def finish_combat(self):
        self.in_combat = False
        opponent = self.current_opponent
        if self.game.player.is_dead:
            self.game.game_over()
        else:
            self.game.player.end_combat(opponent)
            self.game.map.remove_opponent(opponent)

    @classmethod
    def get_hit(cls, attacker, defender):
        diff_lvl = defender.level - attacker.level
        def_ac = (20 - defender.ac) + diff_lvl + defender.ac_modifier
        rng = parse_dice_format(f"1d20+{attacker.hit_modifier}")
        return rng >= def_ac

    @classmethod
    def attack(cls, attacker, defender):
        attack, damage, status_effects = attacker.damage
        if CombatSystem.get_hit(attacker, defender):
            defender.take_damage(damage)
            if status_effects is None:
                print(f"{attacker.name} attacked {defender.name} with {attack} and hit for {damage}!")
            else:
                defender.inflict_status_effects(*status_effects)
                print(f"{attacker.name} attacked {defender.name} with {attack} and hit for {damage}"
                      f"({', '.join(status_effects)})!")
        else:
            print(f"{attacker.name} attacked {defender.name} with {attack} and did not hit!")
