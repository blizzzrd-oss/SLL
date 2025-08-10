
from skills.slash import SlashSkill
from skills.dash import DashSkill

SKILL_REGISTRY = {
    'slash': SlashSkill,
    'dash': DashSkill,
}

def get_skill(name):
    return SKILL_REGISTRY.get(name)
