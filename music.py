import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

class MusicManager:
    def __init__(self):
        self.soundtrack_mute = False
        self.stop_event = None

# Initialise music
def initialise_music():
    pygame.mixer.init()
    return threading.Event()

# Start a music thread
def start_music_thread(stop_event, sound_file, mute=False):
    if mute:
        return
    music_thread = threading.Thread(target=looping_music, args=(stop_event, sound_file), daemon=True)
    music_thread.start()

# Stop the current music thread
def stop_current_music_thread(stop_event):
    stop_event.set()
    time.sleep(0.1)

def change_music(sound_file, stop_event, mute=False):
    stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    start_music_thread(stop_event, sound_file, mute)
    return stop_event

# Looping music
def looping_music(stop_event, sound_file, mute=False):
    if mute:
        return
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Play music in a loop
    while not stop_event.is_set():
        time.sleep(0.1)
    pygame.mixer.music.stop()

# Stop the current music and play a new one
def stop_and_play_music(sound_file, mute=False):
    if mute:
        return
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()