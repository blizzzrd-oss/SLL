"""
Active and passive skills for entities.
"""
class Skill:
    def __init__(self, name, active=True):
        self.name = name
        self.active = active

class ActiveSkill(Skill):
    def __init__(self, name):
        super().__init__(name, active=True)
        # ...active skill logic...

class PassiveSkill(Skill):
    def __init__(self, name):
        super().__init__(name, active=False)
        # ...passive skill logic...
