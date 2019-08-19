from .status_effect import StatusEffect
from .stats import Stats, Job
from .spells import SpellList


class Entity:
    def __init__(self):
        self.status_effects = []
        self.max_health = 10
        self.health = self.max_health
        self.stats = Stats()
        self._job = None
        self.level = 1
        self.spell_list = SpellList(self)

    @property
    def job(self):
        return self._job if self._job is not None else Job(self, "commoner")

    @job.setter
    def job(self, value):
        if isinstance(value, str):
            self._job = Job(self, value)
        elif isinstance(value, Job):
            value.character = self
            self._job = value
        else:
            raise ValueError

    @property
    def saving_throws(self):
        return self.job.saving_throws

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
                status_effect.remove()

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
