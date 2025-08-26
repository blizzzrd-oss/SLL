"""
Headless smoke test for WaveManager event triggering.
Sets all current wave event chances to 1.0 then triggers events and prints pending events.
"""
import pygame
import os

# Ensure local imports work when run directly
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.wave_system import WaveManager
from core.game_modes import GAME_EVENTS
from config import WAVE_EVENT_CHANCES

# Minimal pygame init for any modules that expect it
pygame.display.init()
pygame.display.set_mode((1,1))

def run_test():
    wm = WaveManager(game_mode='Normal')

    # Ensure current wave config is generated
    wm.current_wave_config = wm._generate_wave_config(1)

    # Force all events available in this wave to have chance 1.0
    for en in list(wm.current_wave_config.events):
        wm.current_wave_config.event_chances[en] = 1.0

    # Trigger events
    wm._trigger_wave_events()

    pending = wm.get_pending_events()
    print('Pending events:', pending)

    # Validate types exist in GAME_EVENTS
    all_good = True
    for p in pending:
        t = p.get('type')
        if t not in GAME_EVENTS:
            print(f"MISMATCH: pending event type '{t}' not in GAME_EVENTS")
            all_good = False
        else:
            print(f"OK: pending type '{t}' maps to GAME_EVENTS entry '{GAME_EVENTS[t]['name']}' with multiplier {p.get('multiplier')}.")

    if all_good:
        print('Smoke wave test PASSED: all pending event types match GAME_EVENTS')
    else:
        print('Smoke wave test FAILED: see mismatches above')

if __name__ == '__main__':
    run_test()
