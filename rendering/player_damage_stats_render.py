import pygame

from utils.player_damage_log import PlayerDamageLog

def render_player_damage_stats(screen, player, font):
    damage_log = getattr(player, 'damage_log', None)
    if not isinstance(damage_log, PlayerDamageLog):
        return
    skill_totals_raw = damage_log.skill_totals
    skill_totals_sorted = sorted(skill_totals_raw.items(), key=lambda x: x[1], reverse=True)
    total_damage = sum(skill_totals_raw.values())
    center_x = screen.get_width() // 2
    y = 120
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
    header = small_font.render(f"Player Damage Statistics", True, (255, 255, 0))
    header_rect = header.get_rect(center=(center_x, y))
    screen.blit(header, header_rect)
    y += 30
    for skill, dmg in skill_totals_sorted:
        if isinstance(skill, str):
            skill_name = skill
        elif hasattr(skill, 'name') and isinstance(skill.name, str):
            skill_name = skill.name
        elif hasattr(skill, '__class__') and hasattr(skill.__class__, '__name__'):
            skill_name = skill.__class__.__name__
        else:
            skill_name = 'Unknown'
        line = small_font.render(f"{skill_name}: {damage_log._format_number(dmg)}", True, (255, 255, 255))
        line_rect = line.get_rect(center=(center_x, y))
        screen.blit(line, line_rect)
        y += 32
    total_line = small_font.render(f"Total: {damage_log._format_number(total_damage)}", True, (255, 255, 200))
    total_rect = total_line.get_rect(center=(center_x, y))
    screen.blit(total_line, total_rect)
    y += 40
