import pygame

def text_surface(input_text, font_size=12, color=(255, 255, 255), font_face=None):
    font = pygame.font.Font(font_face, font_size)
    text = font.render(str(input_text), 1, color)
    return text