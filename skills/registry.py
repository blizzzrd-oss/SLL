from skills.slash import SlashSkill

SKILL_REGISTRY = {
    'slash': SlashSkill,
}

def get_skill(name):
    return SKILL_REGISTRY.get(name)
