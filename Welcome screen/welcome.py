import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from tkinter import font as tkFont
import time

# Global variable to keep track of the process
pet_manager_process = None
is_duck_enabled = False

def toggle_duck():
    global pet_manager_process, is_duck_enabled

    if is_duck_enabled:
        if pet_manager_process:
            pet_manager_process.terminate()
            pet_manager_process = None
        duck_button.config(text="Enable Duck")
        is_duck_enabled = False
    else:
        pet_manager_process = subprocess.Popen(["python", "Pet Manager/pet_manager.py"])
        duck_button.config(text="Disable Duck")
        is_duck_enabled = True


def update_background(frame_number):
    global gif_frames
    frame = gif_frames[frame_number]
    background_label.config(image=frame)
    background_label.image = frame  # Keep a reference
    next_frame = (frame_number + 1) % len(gif_frames)
    root.after(20, update_background, next_frame)

# main window
root = tk.Tk()
root.title("Quackii")

#font
nunito = tkFont.Font(family="Nunito", size=18)
josefin = tkFont.Font(family="Josefin Sans", size=42)
josefin2 = tkFont.Font(family="Josefin Sans", size=22)

# Set the window size and position
# Define the window size
window_width = 960
window_height = 540

# Get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center position
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 1.8)

# Set the window position
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

#background
# Set the new dimensions for the GIF
new_width = window_width
new_height = window_height

# Open the GIF file
gif = Image.open("Assets/quackbg.gif")

# Resize each frame and add to the gif_frames list
gif_frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)
    resized_frame = gif.copy().resize((new_width, new_height), Image.Resampling.LANCZOS)
    gif_frames.append(ImageTk.PhotoImage(resized_frame))


# Create a label for the background
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Start the animation
root.after(0, update_background, 0)



duckButtonImage = Image.open("Assets/duckbutton1.png")
duckButtonPhoto = ImageTk.PhotoImage(duckButtonImage)


# Add a button to start the virtual assistant
duck_button = tk.Button(root, text="Enable Duck", command=toggle_duck, font=nunito, image = duckButtonPhoto)
duck_button.pack(pady=45)

# Start the Tkinter event loop
root.mainloop()