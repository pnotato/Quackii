import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from tkinter import font as tkFont
import time
import asyncio
import os

# Global variable to keep track of the process
pet_manager_process = None
is_duck_enabled = False

def show_frame(frame):
    frame.tkraise()

def toggle_duck():
    global pet_manager_process, is_duck_enabled, button_photo_enable, button_photo_disable

    if is_duck_enabled:
        if pet_manager_process:
            pet_manager_process.terminate()
            pet_manager_process = None
        duck_button.config(image=duckButtonPhoto)
        is_duck_enabled = False
    else:
        pet_manager_process = subprocess.Popen(["python3", "pet_manager.py"])
        duck_button.config(image=duckButtonPhoto2)
        is_duck_enabled = True


def update_background(frame_number):
    global gif_frames
    frame = gif_frames[frame_number]
    background_label.config(image=frame)
    background_label.image = frame  # Keep a reference
    next_frame = (frame_number + 1) % len(gif_frames)
    main_frame.after(20, update_background, next_frame)



# main window
root = tk.Tk()
root.title("Quackii")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames
main_frame = tk.Frame(root)
credits_frame = tk.Frame(root)

for frame in (main_frame, credits_frame):
    frame.grid(row=0, column=0, sticky='nsew')


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
background_label = tk.Label(main_frame)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Start the animation
root.after(0, update_background, 0)





duckButtonImage = Image.open("Assets/duckbutton1.png")
duckButtonPhoto = ImageTk.PhotoImage(duckButtonImage)

duckButtonImage2 = Image.open("Assets/duckbutton2.png")
duckButtonPhoto2 = ImageTk.PhotoImage(duckButtonImage2)

chatBI = Image.open("Assets/chatbutton.png")
chatBP = ImageTk.PhotoImage(chatBI)

toolBI = Image.open("Assets/toolboxbutton.png")
toolBP = ImageTk.PhotoImage(toolBI)

credBI = Image.open("Assets/creditsbutton.png")
credBP = ImageTk.PhotoImage(credBI)


# Add a button to start the virtual assistant
duck_button = tk.Button(main_frame,image = duckButtonPhoto, command=toggle_duck)
duck_button.place(x = 390,y=260)

chat_button = tk.Button(main_frame, image=chatBP, command=lambda: show_frame(chat_frame))
chat_button.place(x = 150,y=260)

tool_button = tk.Button(main_frame, image=toolBP)
tool_button.place(x = 630,y=260)

cred_button = tk.Button(main_frame, image=credBP, text="Credits", command=lambda: show_frame(credits_frame))
cred_button.place(x = 390,y=430)

# Credits Frame
credits_label = tk.Label(credits_frame, text="Credits\n\nPerson 1\nPerson 2\nPerson 3")
credits_label.pack(pady=10)

back_button = tk.Button(credits_frame, text="Back", command=lambda: show_frame(main_frame))
back_button.pack()

# Chat Frame

# add an input box to submit text
input_box = tk.Entry(chat_frame, width=50)
input_box.pack(pady=10)

# add a button to submit text
submit_button = tk.Button(chat_frame, text="Submit", command=lambda: submit_text())
submit_button.pack()

# add a button to go back to the main frame
back_button = tk.Button(chat_frame, text="Back", command=lambda: show_frame(main_frame))
back_button.pack()

# when you submit text, call the pet manager's chat function
def submit_text():
    global input_box
    text = input_box.get()
    input_box.delete(0, tk.END)

    # create new txt file if one does not exist already, and replace the text in the file with the new text
    if not os.path.exists("chat.txt"):
        open("chat.txt", "w").close()
    with open("chat.txt", "w") as f:
        f.write(text)

    

show_frame(main_frame)

# Start the Tkinter event loop
root.mainloop()