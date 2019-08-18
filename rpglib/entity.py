from .status_effect import StatusEffect


class Entity:
    def __init__(self):
        self.status_effects = []
        self.health = 0

    @property
    def is_dead(self):
        return self.health <= 0

    def take_damage(self, amount):
        self.health -= amount

    def inflict_status_effects(self, *status_effects):
        status_effects = list(status_effects)
        for i, effect in enumerate(status_effects):
            status_effects[i] = StatusEffect(effect, self)
        self.status_effects.extend(status_effects)
        self.status_effects = list(set(self.status_effects))

    def apply_status_effects(self):
        for status_effect in self.status_effects:
            status_effect.apply()
            if status_effect.reached_timeout:
                self.status_effects.remove(status_effect)