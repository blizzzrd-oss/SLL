"""
Shared components for entities (e.g., health, position).
"""
class HealthComponent:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health
