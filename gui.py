from tkinter import *
import music

soundtrack_mute = False

def start_screen():
    global soundtrack_mute
    stop_event = music.initialise_music()
    music.start_music_thread(stop_event, "music/cats.wav", soundtrack_mute)
    window = Tk()
    window.title("Terra Incognita")
    window.geometry("600x600")
    button = Button(window, text="Change Music", command=lambda : music.change_music("music/riff.wav", stop_event, soundtrack_mute))
    button.pack(padx=10, pady=10)
    window.mainloop()