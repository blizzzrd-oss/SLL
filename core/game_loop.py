"""
Main game loop implementation.
Orchestrates all game systems with clean separation of concerns.
"""

import pygame
from core.player_movement import handle_player_movement, get_movement_vector
from core.init import initialize_game_state
from rendering.game_render import draw_game, invalidate_pause_cache
from core.event_handler import GameEventHandler
from core.game_logic import GameLogicManager
from core.frame_timer import FrameTimer
from ui.loading_screen import show_loading_screen
from ui.enhancement_selection import EnhancementSelectionUI
from rendering.background_render import print_cache_stats, generate_new_world


def run_game(screen, slot, mode):
    """
    Main game loop with clean architecture.
    
    Args:
        screen: Pygame display surface
        slot: Save slot index
        mode: Game difficulty mode ('Easy', 'Normal', 'Hard')
    """
    # Show loading screen and preload map tiles
    print(f"Starting game with mode: {mode}")
    print("Generating new world...")
    
    # Generate a new world with random seed
    generate_new_world()
    
    print("Showing loading screen...")
    
    # Define loading steps
    def load_sounds():
        """Load game sounds."""
        from audio.sound_manager import SoundManager
        SoundManager.preload_all_sounds()
    
    def load_world():
        """Load world map tiles."""
        from rendering.background_render import preload_map_tiles
        from config import WORLD_SIZE, TILE_SIZE
        preload_map_tiles(WORLD_SIZE, TILE_SIZE, None)
    
    def initialize_systems():
        """Initialize game systems."""
        # Any additional initialization can go here
        pass
    
    loading_steps = [
        ("Sounds", load_sounds),
        ("World Map", load_world),
        ("Game Systems", initialize_systems)
    ]
    
    # Preload with step-based loading
    loading_success = show_loading_screen(
        screen, 
        loading_steps=loading_steps,
        preload_type="full", # area, full
        spawn_x=0,  # Spawn at world center
        spawn_y=0, 
        radius_tiles=300  # Adjust this based on how much you want to preload
    )
    
    if not loading_success:
        print("Loading failed, continuing without preload...")
    else:
        print("Loading successful!")
        print_cache_stats()
    
    # Initialize game state
    (
        game, running, should_exit, last_move, time_accum, clock, paused, pause_menu_selected,
        pause_menu_options, pause_menu_rects, in_settings_menu, settings_menu, hud_visible, settings_path
    ) = initialize_game_state(screen, slot, mode)
    
    # Initialize system managers
    event_handler = GameEventHandler(game, screen)
    game_logic = GameLogicManager(game, screen)
    frame_timer = FrameTimer(settings_path)
    enhancement_ui = EnhancementSelectionUI(screen)
    
    # Connect enhancement UI to player for pickable system
    game.player.enhancement_ui = enhancement_ui
    
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
    was_paused = False
    while event_handler.running:
        # Get frame timing
        dt, time_accum, fps = frame_timer.tick()
        
        # Check for enhancement selection first
        if (game.player.has_pending_enhancement_selection() and not enhancement_ui.is_active):
            choices = game.player.get_enhancement_choices()
            if choices:
                # Don't reset reroll charges - they persist and come from pickables
                # Create reroll callback that generates new choices
                def reroll_callback():
                    return game.player.get_enhancement_choices()
                enhancement_ui.show_enhancement_selection(choices, reroll_callback)
        
        # Handle enhancement selection events (priority over normal events)
        if enhancement_ui.is_active:
            for event in pygame.event.get():
                selected_enhancement = enhancement_ui.handle_event(event)
                if selected_enhancement and selected_enhancement != "reroll":
                    game.player.apply_enhancement_choice(selected_enhancement)
                    enhancement_ui.close()
                    # Clear stuck key states when enhancement UI closes
                    event_handler.clear_all_key_states()
                    print(f"[ENHANCEMENT] Selected: {selected_enhancement}")
                elif selected_enhancement == "reroll":
                    print(f"[ENHANCEMENT] Rerolled choices")
                    # The reroll is already handled in the UI, just continue
            
            # Render game background using pause cache system (without pause overlay)
            from rendering.game_render import _pause_screen_cache, _pause_cache_valid, render_full_game_to_cache
            
            if _pause_cache_valid and _pause_screen_cache:
                # Use cached game screen
                screen.blit(_pause_screen_cache, (0, 0))
            else:
                # Cache is invalid - render full game and cache it  
                render_full_game_to_cache(screen, game, last_move, time_accum, 
                                        event_handler.hud_visible, fps, 
                                        game_logic.game_time, game_logic.get_wave_info())
            
            # Render enhancement UI on top
            enhancement_ui.render()
            pygame.display.flip()
            continue
        
        # Handle settings menu (priority after enhancement UI)
        if event_handler.in_settings_menu:
            # Handle events first (this is done in handle_all_events)
            event_handler.handle_all_events()
            # Then render settings menu
            if event_handler.show_settings_menu_if_active():
                pygame.display.flip()
                continue
        
        # Handle all input events (only when enhancement UI and settings menu are not active)
        event_handler.handle_all_events()
        
        # Check for pause state change to invalidate cache
        if was_paused and not event_handler.paused:
            # Just unpaused - invalidate cache so game renders fresh
            invalidate_pause_cache()
        was_paused = event_handler.paused
            
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
            fps=fps,
            game_time=game_logic.game_time,
            wave_info=game_logic.get_wave_info()
        )
        
        # Check for exit condition
        if event_handler.should_exit:
            break
