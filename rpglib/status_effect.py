import json
from .utils import parse_dice_format


class StatusEffect:
    def __init__(self, name, target):
        self.name = name
        self.target = target
        self._counter = 0

        with open("data/status_effects.json") as f:
            data = json.load(f).get(name, {})

        self.timeout = data.get("timeout", 1)
        self.effect = data.get("effect", "")

    def apply(self):
        effect_type, effect_value = self.effect.split(":")
        effect_type = effect_type.lower()
        self._counter += 1

        if effect_type == "dmg":
            self.target.take_damage(parse_dice_format(effect_value))
            return
        else:
            return

    @property
    def reached_timeout(self):
        return self._counter >= self.timeout
