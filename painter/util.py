def render_text(screen, font, text, posx, posy):
    text = font.render(text, True, (0, 128, 0))
    screen.blit(text, (posx - text.get_width() // 2, posy - text.get_height() // 2))
