"""
Player entity and logic.
"""
class Player:
    def __init__(self):
        self.health = 100
        self.position = (0, 0)
        self.damage_log = []
        self.recent_damage = []
        # ...other attributes...

    def take_damage(self, amount, source):
        self.health -= amount
        self.damage_log.append((amount, source))
        self.recent_damage.append((amount, source))
        # ...handle death, clear recent_damage, etc...
