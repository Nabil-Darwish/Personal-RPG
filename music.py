import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

# Initialise music
def initialise_music():
    pygame.mixer.init()
    return threading.Event()

# Start a music thread
def start_music_thread(stop_event, sound_file):
    music_thread = threading.Thread(target=looping_music, args=(stop_event, sound_file), daemon=True)
    music_thread.start()

# Stop the current music thread
def stop_current_music_thread(stop_event):
    stop_event.set()
    time.sleep(0.1)

# Looping music
def looping_music(stop_event, sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Play music in a loop
    while not stop_event.is_set():
        time.sleep(0.1)
    pygame.mixer.music.stop()

# Stop the current music and play a new one
def stop_and_play_music(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()