import tkinter as tk
import asyncio

class Pet:
    def __init__(self):
        # Create empty window
        self.window = tk.Tk()
        self.window.resizable(0, 0)

        # Disable window background and make it transparent
        self.window.overrideredirect(1)
        self.window.wm_attributes("-transparentcolor", "black")

        # Create canvas, position at bottom center, and pack
        self.canvas = tk.Canvas(self.window, width=500, height=500, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Create pet using image from assets folder
        self.start_frame = tk.PhotoImage(file="Assets/idle1.png")
        self.current_frame = self.canvas.create_image(250, 250, image=self.start_frame)

        # Initialize animations
        self.run_animation = [tk.PhotoImage(file="Assets/running" + f"{i}" + ".png") for i in range(1, 4)]
        self.idle_animation = [tk.PhotoImage(file="Assets/idle" + f"{i}" + ".png") for i in range(1, 3)]
        self.grabbed_animation = [tk.PhotoImage(file="Assets/grabbed" + f"{i}" + ".png") for i in range(1, 3)]

        # Initialize frame and animation variables
        self.frame = 0
        self.current_animation = self.run_animation

        self.update()

    def update(self):
        # ANIMATION ------------------------------------
        # Change animation frame based on current animation 
        if self.current_animation == self.run_animation:
            print(f"Playing frame {self.frame} of run animation")
            self.canvas.itemconfig(self.current_frame, image=self.run_animation[self.frame])
        elif self.current_animation == self.idle_animation:
            print(f"Playing frame {self.frame} of idle animation")
            self.canvas.itemconfig(self.current_frame, image=self.idle_animation[self.frame])
        elif self.current_animation == self.grabbed_animation:
            print(f"Playing frame {self.frame} of grabbed animation")
            self.canvas.itemconfig(self.current_frame, image=self.grabbed_animation[self.frame])
            
        # Increment frame
        self.frame += 1
        self.frame %= len(self.current_animation)
        self.canvas.update()

    def play_animation(self, animation):
        # Change current animation and reset frame
        self.current_animation = animation
        self.frame = 0

    def say(self, text):
        # Create new top level window
        speech_window = tk.Toplevel(self.window)
        speech_window.resizable(0, 0)

        # Remove close/minimize bar on the top
        speech_window.overrideredirect(1)

        # Create speech bubble background (rounded white rectangle)
        speech_bubble = tk.Canvas(speech_window, width=300, height=100, bg="white", highlightthickness=0)
        speech_bubble.create_rectangle(0, 0, 300, 100, fill="white", outline="white")

        # Create text
        speech_text = tk.Label(speech_bubble, text=text, font=("Arial", 12), wraplength=280, justify="center")
        speech_text.pack()

        # Pack speech bubble after packing the text
        speech_bubble.pack()

        # Resize window to fit text on screen
        speech_window.update()
        speech_window.geometry(f"{speech_bubble.winfo_width()}x{speech_bubble.winfo_height()}")

        # Destroy the window after a time proportional to the length of the text
        speech_window.after(int(len(text) * 100), speech_window.destroy)

