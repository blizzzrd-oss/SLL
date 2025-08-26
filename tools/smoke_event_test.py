"""
Headless smoke test for GameEvent behavior.
Creates a Game instance, forces events, and prints multipliers.
"""
import time
from core.game import Game
import pygame

# Initialize a dummy pygame display to satisfy modules that require it
pygame.display.init()
pygame.display.set_mode((1,1))

def run_test():
    game = Game(screen=None, slot=None, mode='Normal')
    em = game.event_manager

    print('Active events before:', em.get_active_events_display())

    # Force Loot Blessing (bonus_loot_event key in GAME_EVENTS is 'bonus_loot_event')
    em.force_event('bonus_loot_event')
    # Force Enemy Weakness event
    em.force_event('enemy_weakness_event')

    print('Active events after forcing:')
    for e in em.get_active_events_display():
        print(' -', e)

    multipliers = em.get_active_multipliers()
    print('Multipliers:', multipliers)

    # Check effective damage scaling
    base = 10
    effective = game.get_effective_damage(base)
    print(f'Base damage {base} -> effective {effective}')

if __name__ == '__main__':
    run_test()
