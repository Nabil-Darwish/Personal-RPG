import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

class MusicManager:
    def __init__(self, soundtrack_mute=False):
        self.soundtrack_mute = soundtrack_mute
        self.stop_event = self.initialise_music()

    # Initialise music
    def initialise_music(self):
        pygame.mixer.init()
        return threading.Event()

    # Start a music thread
    def start_music_thread(self, sound_file):
        if self.soundtrack_mute:
            return
        music_thread = threading.Thread(target=self.looping_music, args=(sound_file,), daemon=True)
        music_thread.start()

    # Stop the current music thread
    def stop_current_music_thread(self):
        self.stop_event.set()
        time.sleep(0.1)
        self.stop_event.clear()

    def change_music(self, sound_file):
        self.stop_current_music_thread()
        self.start_music_thread(sound_file)

    # Looping music
    def looping_music(self, sound_file):
        if self.soundtrack_mute:
            return
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(-1)  # Play music in a loop
        while not self.stop_event.is_set():
            time.sleep(0.1)
        pygame.mixer.music.stop()

    # Stop the current music and play a new one
    def stop_and_play_music(self, sound_file):
        if self.soundtrack_mute:
            return
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    # toggles soundtrack mute
    def toggle_soundtrack_mute(self):
        self.soundtrack_mute = not self.soundtrack_mute