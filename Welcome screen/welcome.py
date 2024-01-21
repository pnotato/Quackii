import tkinter as tk
import subprocess
from tkinter import font as tkFont

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


# main window
root = tk.Tk()
root.title("Quackii")

#font
nunito = tkFont.Font(family="Nunito", size=18)
josefin = tkFont.Font(family="Josefin Sans", size=42)

# Set the window size and position
# Define the window size
window_width = 600
window_height = 400

# Get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center position
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 1.5)

# Set the window position
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')





# Add a welcome message
welcome_label = tk.Label(root, text="Quackii", font=josefin)
welcome_label.pack(pady=20)

# Add a button to start the virtual assistant
duck_button = tk.Button(root, text="Enable Duck", command=toggle_duck, font=nunito)
duck_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()