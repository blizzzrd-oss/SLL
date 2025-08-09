"""
Comprehensive damage log logic.
"""
class DamageLog:
    def __init__(self):
        self.entries = []

    def add_entry(self, amount, source, target, timestamp):
        self.entries.append({
            'amount': amount,
            'source': source,
            'target': target,
            'timestamp': timestamp
        })

    def get_recent(self, count=10):
        return self.entries[-count:]
