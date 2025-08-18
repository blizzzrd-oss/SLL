"""
Player received log: tracks damage/heal events received by the player.
"""
from collections import deque
from datetime import datetime
from config import PLAYER_RECEIVED_LOG_MAX_ENTRIES

class PlayerReceivedLog:
    def __init__(self):
        self.entries = deque(maxlen=PLAYER_RECEIVED_LOG_MAX_ENTRIES)

    def add_entry(self, amount, source, type_, health=None, barrier=None):
        time_str = datetime.now().strftime('%H:%M:%S')
        self.entries.append({
            'amount': amount,
            'source': source,
            'type': type_,  # 'damage' or 'heal'
            'timestamp': time_str,
            'health': health,
            'barrier': barrier
        })

    def get_recent(self):
        return list(self.entries)

    def _format_number(self, n):
        return f"{n:,}".replace(",", ".")
