# utils/text.py
def draw_centered_text(screen, font, text, y, color):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(centerx=screen.get_width() // 2)
    rect.y = y
    screen.blit(rendered, rect)
    return rect.height
