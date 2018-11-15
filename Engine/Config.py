import pygame
import os

screen_width = 1280
screen_height = 720
save_game_path = ["RPG", "saves"]
video_scale = 1

def get_save_path():
	return os.path.join(*save_game_path)

def set_video_scale(scale):
    global video_scale
    video_scale = scale

def get_video_scale():
    return video_scale

def set_screensize(w, h):
	global screen_width, screen_height
	screen_width = w
	screen_height = h

def get_screensize():
	return (screen_width, screen_height)

def get_screenrect():
    return pygame.Rect(0, 0, screen_width, screen_height)