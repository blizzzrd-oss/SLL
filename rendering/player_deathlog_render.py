import pygame

def render_player_deathlog(screen, player, font):
    received_log = getattr(player, 'received_log', None)
    if not received_log:
        return
    recent = received_log.get_recent()
    center_x = screen.get_width() // 2
    y2 = screen.get_height() // 2
    # Try to create a smaller font based on the original font's properties
    try:
        font_path = font.name if hasattr(font, 'name') else None
        font_size = font.get_height()
        small_size = max(12, font_size - 4)
        if font_path:
            small_font = pygame.font.Font(font_path, small_size)
        else:
            # Fallback to SysFont with same family if possible
            small_font = pygame.font.SysFont(None, small_size)
    except Exception:
        small_font = pygame.font.SysFont(None, max(12, font.get_height() - 4))
    header2 = small_font.render(f"Deathlog:", True, (255, 180, 180))
    header2_rect = header2.get_rect(center=(center_x, y2))
    screen.blit(header2, header2_rect)
    y2 += 30
    for entry in recent:
        hp = entry.get('health', 0)
        barrier = entry.get('barrier', 0)
        # Use the max health/barrier that was current when this entry was recorded
        max_hp = entry.get('max_health', getattr(player, 'max_health', 100))
        max_barrier = entry.get('max_barrier', getattr(player, 'max_barrier', 100))
        hp_str = f"{int(max(0, hp))}/{int(max_hp)}"
        barrier_str = f"{int(max(0, barrier))}/{int(max_barrier)}"
        if entry['type'] == 'damage':
            color = (255, 80, 80)
            change_type = "-" + str(int(abs(entry['amount'])))
        else:
            color = (80, 255, 80)
            change_type = "+" + str(int(entry['amount']))
        src = entry['source']
        src_str = None
        if hasattr(src, 'enemy_type') and isinstance(src.enemy_type, str):
            src_str = src.enemy_type
        elif isinstance(src, str):
            src_str = src
        elif hasattr(src, 'name') and isinstance(src.name, str):
            src_str = src.name
        elif hasattr(src, '__class__') and hasattr(src.__class__, '__name__'):
            src_str = src.__class__.__name__
        else:
            src_str = str(src)
        if src_str and src_str.startswith('<') and 'object at' in src_str:
            src_str = src_str.split('object at')[0].replace('<', '').replace('>', '').strip()
        time_str = entry.get('timestamp', '')
        line_txt = f"[{time_str}] {change_type} {'barrier' if 'barrier' in src_str.lower() else 'health'} by {src_str} - hp:{hp_str} barrier:{barrier_str}"
        line = small_font.render(line_txt, True, color)
        line_rect = line.get_rect(center=(center_x, y2))
        screen.blit(line, line_rect)
        y2 += 32
    if player.health <= 0:
        death_line = small_font.render("DEATH", True, (255, 0, 0))
        death_rect = death_line.get_rect(center=(center_x, y2))
        screen.blit(death_line, death_rect)
