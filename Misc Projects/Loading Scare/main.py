import tkinter as tk
from tkinter import ttk
import pygame
import os

root = tk.Tk()
root.title('Progress Bar')
root.geometry('1920x1080')

percentage = 0
increment = 0.01
delay = 50  # Initial delay between each update

style = ttk.Style()
style.theme_use('xpnative')

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=800, mode='determinate')
progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

progress_label = tk.Label(root, font=('Arial', 20), fg='black')
progress_label.place(relx=0.5, rely=0.5, y=-30, anchor=tk.CENTER)

watermark_label = tk.Label(root, text='@Satnav_boom', font=('Arial', 12), fg='light grey')
watermark_label.place(relx=0.5, rely=0.5, y=25, anchor=tk.CENTER)

# Get the directory path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the sound files in the same directory
background_sound_file = os.path.join(script_dir, 'background-noise.wav')
scare_sound_file = os.path.join(script_dir, 'scare.wav')

pygame.mixer.init()

# Load and play the background music once
pygame.mixer.music.load(background_sound_file)
pygame.mixer.music.set_volume(0.02)  # Set the volume to a low level
pygame.mixer.music.play(0)  # Play the background music once

def update_progress_bar():
    global percentage, progress_bar, progress_label, delay
    
    if percentage < 99:
        increment = (100 - percentage) / 1000  # Calculate the dynamic increment based on remaining progress
        percentage += increment
    
    progress_bar['value'] = percentage
    progress_label.config(text=f"{int(percentage)}%")
    progress_bar.update()
    
    if percentage >= 99:
        delay += 10  # Increase the delay after reaching 99%
    
    if delay < 27000:  # Delay for 27 seconds (27000 milliseconds)
        root.after(10, update_progress_bar)
    else:
        play_scare_sound()

def play_scare_sound():
    pygame.mixer.music.stop()  # Stop the background music
    pygame.mixer.music.load(scare_sound_file)  # Load the scare sound
    pygame.mixer.music.set_volume(2)  # Set the volume to 2 (louder)
    pygame.mixer.music.play()  # Play the scare sound

update_progress_bar()

root.mainloop()
