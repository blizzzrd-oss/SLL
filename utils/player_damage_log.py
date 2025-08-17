"""
Player damage log: tracks all outgoing damage, grouped by skill, with formatted numbers.
"""
from collections import defaultdict

class PlayerDamageLog:
    def __init__(self):
        self.entries = []  # List of all damage events
        self.skill_totals = defaultdict(int)  # Total damage per skill

    def add_entry(self, amount, skill, target):
        self.entries.append({
            'amount': amount,
            'skill': skill,
            'target': target
        })
        self.skill_totals[skill] += amount


    def get_total_by_skill(self, skill):
        return self.skill_totals[skill]

    def get_all_skill_totals(self):
        return {k: self._format_number(v) for k, v in self.skill_totals.items()}

    def get_total_damage(self):
        return self._format_number(sum(self.skill_totals.values()))

    def _format_number(self, n):
        return f"{n:,}".replace(",", ".")
