"""
Clean game loop implementation.
Orchestrates all game systems with clear separation of concerns.
"""

import pygame
from core.player_movement import handle_player_movement, get_movement_vector
from core.init import initialize_game_state
from rendering.game_render import draw_game
from core.event_handler import GameEventHandler
from core.game_logic import GameLogicManager
from core.frame_timer import FrameTimer


def run_game(screen, slot, mode):
    """
    Main game loop with clean architecture.
    
    Args:
        screen: Pygame display surface
        slot: Save slot index
        mode: Game difficulty mode ('Easy', 'Normal', 'Hard')
    """
    # Initialize game state
    (
        game, running, should_exit, last_move, time_accum, clock, paused, pause_menu_selected,
        pause_menu_options, pause_menu_rects, in_settings_menu, settings_menu, hud_visible, settings_path
    ) = initialize_game_state(screen, slot, mode)
    
    # Initialize system managers
    event_handler = GameEventHandler(game, screen)
    game_logic = GameLogicManager(game, screen)
    frame_timer = FrameTimer(settings_path)
    
    # Sync initial state with event handler
    event_handler.running = running
    event_handler.should_exit = should_exit
    event_handler.paused = paused
    event_handler.pause_menu_selected = pause_menu_selected
    event_handler.pause_menu_options = pause_menu_options
    event_handler.pause_menu_rects = pause_menu_rects
    event_handler.in_settings_menu = in_settings_menu
    event_handler.settings_menu = settings_menu
    event_handler.hud_visible = hud_visible
    
    # Main game loop
    while event_handler.running:
        # Get frame timing
        dt, time_accum, fps = frame_timer.tick()
        
        # Handle all input events
        event_handler.handle_all_events()
        
        # Skip rest of frame if in settings menu
        if event_handler.show_settings_menu_if_active():
            continue
            
        # Handle player movement
        if not game.game_over and not event_handler.paused:
            move_dx, move_dy = get_movement_vector()
            
            # Update player movement state
            if (move_dx, move_dy) != (0, 0):
                game.player.last_move = (move_dx, move_dy)
            last_move = (move_dx, move_dy)
            
            # Apply movement
            handle_player_movement(game.player, dt)
        
        # Update game logic
        game_logic.update(dt, event_handler)
        
        # Render everything
        draw_game(
            screen=screen,
            game=game,
            last_move=last_move,
            time_accum=time_accum,
            paused=event_handler.paused,
            pause_menu_selected=event_handler.pause_menu_selected,
            pause_menu_options=event_handler.pause_menu_options,
            pause_menu_rects=event_handler.pause_menu_rects,
            hud_visible=event_handler.hud_visible,
            fps=fps
        )
        
        # Check for exit condition
        if event_handler.should_exit:
            break


# Backwards compatibility - keep original function signature
def run_game_legacy(screen, slot, mode):
    """Legacy wrapper for the original game loop function."""
    return run_game(screen, slot, mode)
