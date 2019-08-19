import json
from .utils import parse_dice_format
from .stats import Stats


class StatusEffect:
    def __init__(self, name, target):
        self.name = name
        self.target = target
        self._counter = 0

        with open("data/status_effects.json") as f:
            data = json.load(f).get(name, {})

        self.timeout = data.get("timeout", 1)
        self.effects = list(data.get("effect", ""))

    def apply(self):
        self._counter += 1
        for effect in self.effects:
            effect_type, effect_value = effect.split(":")
            effect_type = effect_type.lower()

            if effect_type == "dmg":
                self.target.take_damage(parse_dice_format(effect_value))
            elif effect_type in Stats.stat_names:
                self.target.stats[effect_type].temp_stat_modifier += int(effect_value)
            elif effect_type == "heal":
                self.target.heal(parse_dice_format(effect_value))

    @property
    def reached_timeout(self):
        return self._counter >= self.timeout

    def remove(self):
        for effect in self.effects:
            effect_type, effect_value = effect.split(":")
            effect_type = effect_type.lower()
            if effect_type in Stats.stat_names:
                self.target.stats[effect_type].temp_stat_modifier -= int(effect_value)
