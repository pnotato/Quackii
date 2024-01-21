import tkinter as tk
import asyncio
import numpy as np
from PIL import Image, ImageTk
import random
import Chat.chat as chat
import pygame

class Pet:
    def __init__(self):
        # WINDOW ---------------------------------------
        # Create empty window
        self.window = tk.Tk()
        self.window.resizable(0, 0)

        # Disable window background and make it transparent
        self.window.overrideredirect(1)
        self.window.wm_attributes("-transparent", "orange") # change orange to True if on macos

        # Create canvas, position at bottom center, and pack
        self.canvas = tk.Canvas(self.window, width=300, height=300, bg="orange", highlightthickness=0)
        self.window.attributes("-topmost", True)
        self.canvas.pack()

        # Create pet using image from assets folder
        self.start_frame = Image.open("Assets/idle1.png")
        self.start_frame = ImageTk.PhotoImage(self.start_frame)
        self.current_frame = self.canvas.create_image(150, 150, image=self.start_frame)

        # Initialize animations (normal and flipped)
        self.run_animation = [Image.open("Assets/running" + f"{i}" + ".png") for i in range(1, 4)]
        self.idle_animation = [Image.open("Assets/idle" + f"{i}" + ".png") for i in range(1, 2)]
        self.grabbed_animation = [Image.open("Assets/grabbed" + f"{i}" + ".png") for i in range(1, 3)]

        # Make images twice as small
        self.run_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.run_animation]
        self.idle_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.idle_animation]
        self.grabbed_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.grabbed_animation]

        # Flip the images horizontally
        self.run_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.run_animation]
        self.idle_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.idle_animation]  # Add this line
        self.grabbed_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.grabbed_animation]  # Add this line

        self.run_animation = [ImageTk.PhotoImage(image) for image in self.run_animation]
        self.run_animation_flipped = [ImageTk.PhotoImage(image) for image in self.run_animation_flipped]
        self.idle_animation = [ImageTk.PhotoImage(image) for image in self.idle_animation]
        self.idle_animation_flipped = [ImageTk.PhotoImage(image) for image in self.idle_animation_flipped]  # Add this line
        self.grabbed_animation = [ImageTk.PhotoImage(image) for image in self.grabbed_animation]
        self.grabbed_animation_flipped = [ImageTk.PhotoImage(image) for image in self.grabbed_animation_flipped]  # Add this line
                
        # Initialize frame and animation variables
        self.frame = 0
        self.frame_rounded = 0
        self.current_animation = self.run_animation

        # PHYSICS --------------------------------------
        # Initialize velocity and acceleration
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        # BIND MOUSE EVENTS ------------------------------
        # Bind mouse events to window for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<ButtonPress-3>", self.begin_chat)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

        self.isDragged = False
        self.isTalking = False

        self.chat_manager = chat.chatManager()

        self.update()

    def update(self):
        # ANIMATION ------------------------------------
        # Change animation frame based on current animation and velocity
        if self.velocity[0] > 0:
            # Moving right
            self.current_animation = self.run_animation_flipped
        elif self.velocity[0] < 0:
            # Moving left
            self.current_animation = self.run_animation

        #print(f"Playing frame {self.frame} of animation")
        self.canvas.itemconfig(self.current_frame, image=self.current_animation[self.frame_rounded])

        # Increment frame
        self.frame += 0.1
        self.frame_rounded = int(self.frame)
        self.frame_rounded %= len(self.current_animation)
        self.canvas.update()

        # PHYSICS --------------------------------------
        # Update acceleration based on gravity
        if not self.isDragged:
            self.acceleration = np.array([0, 4])
        else:
            self.acceleration = np.array([0, 0])

        # Update velocity based on acceleration
        self.velocity += self.acceleration

        # Update position of window based on velocity
        x = int(self.window.winfo_x() + self.velocity[0])
        y = int(self.window.winfo_y() + self.velocity[1])
        self.window.geometry(f"+{x}+{y}")

        # If the pet reaches the bottom of the screen, freeze y velocity
        bottom = self.window.winfo_screenheight() - self.window.winfo_height()
        if y > bottom:
            self.velocity[1] = 0
            self.window.geometry(f"+{x}+{bottom}")

        # If the pet reaches the edges of the screen, freeze x velocity
        left = 0
        right = self.window.winfo_screenwidth() - self.window.winfo_width()
        if x < left:
            self.velocity[0] = 0
            self.window.geometry(f"+{left}+{y}")
        elif x > right:
            self.velocity[0] = 0
            self.window.geometry(f"+{right}+{y}")

    def play_animation(self, animation):
        # Change current animation and reset frame
        self.current_animation = animation
        self.frame = 0
        self.frame_rounded = 0


    def on_drag_start(self, event):
        # Record the starting position of the mouse when clicked
        if not self.isTalking:
            self.start_x = event.x_root
            self.start_y = event.y_root

            self.isDragged = True
            self.play_animation(self.grabbed_animation)

    def on_drag_motion(self, event):
        if not self.isTalking:
            # Calculate the movement of the mouse
            delta_x = event.x_root - self.start_x
            delta_y = event.y_root - self.start_y

            # set pet's velocity and acceleration to zero
            self.set_velocity([0, 0])
            self.set_acceleration([0, 0])

            # Move the window accordingly
            self.window.geometry(f"+{self.window.winfo_x() + delta_x}+{self.window.winfo_y() + delta_y}")

            # Update the starting position for the next movement
            self.start_x = event.x_root
            self.start_y = event.y_root

    def on_drag_release(self, event):
        self.isDragged = False

    def begin_chat(self, event):
        # open a new top level window for the chat
        chat_window = tk.Toplevel(self.window)
        chat_window.resizable(0, 0)

        # change background color of window to yellow
        chat_window.configure(bg="#dba40b")

        # configure the font size and style
        font = ("Arial", 12)

        # add an input box with larger font size
        input_box = tk.Entry(chat_window, width=50, font=font)
        input_box.pack(side="left", padx=10, pady=10)

        # add a send button with larger font size and modern design
        send_button = tk.Button(chat_window, text="Ask Quackii!", font=font, bg="#1f1f1f", fg="white", relief="flat", command=lambda: self.chat(input_box.get()))
        send_button.pack(side="left", padx=10, pady=10)

        # update the window
        chat_window.update()

    def chat(self, text):
        self.say(self.chat_manager.send_message(text))
        self.idle()
        

    def set_velocity(self, velocity):
        self.velocity = np.array(velocity)

    def set_acceleration(self, acceleration):
        self.acceleration = np.array(acceleration)

    def idle(self):
        if self.velocity[0] > 0:
            self.play_animation(self.idle_animation_flipped)
        else:
            self.play_animation(self.idle_animation)

        self.set_velocity([0, self.velocity[1]])
        self.set_acceleration([0, self.acceleration[1]])

    def say(self, text):
        if not self.isTalking:

            self.play_sound("Assets/animalese.mp3")

            self.isTalking = True

            # Create new top-level window
            speech_window = tk.Toplevel(self.window)
            speech_window.bind("<Destroy>", self.stop_sound)
            speech_window.resizable(0, 0)

            # Remove close/minimize bar on the top
            speech_window.overrideredirect(1)
            
            # make the speech bubble always on top
            speech_window.attributes("-topmost", True)
            speech_window.wm_attributes("-transparent", "yellow") # change white to True if on macos

            # Create speech bubble background (rounded white rectangle)
            bubble_width = 300  # Adjust the width as needed
            bubble_height = 200  # Adjust the height as needed
            speech_bubble = tk.Canvas(speech_window, width=bubble_width, height=bubble_height, bg="yellow", highlightthickness=0)

            # Calculate pet's position on the screen
            pet_position = self.window.winfo_x() + self.window.winfo_width() / 2, self.window.winfo_y() + self.window.winfo_height() / 2

            # Calculate speech bubble position over the pet
            speech_x = pet_position[0] - bubble_width / 2  # Adjust the positioning as needed
            speech_y = pet_position[1] - bubble_height - 75  # Adjust the positioning as needed

            # Create rectangle and triangle for speech bubble
            #speech_bubble.create_rectangle(0, 0, bubble_width, bubble_height - 25, fill="white", outline="white", width=2)

            # create rounded rectangle with polygon
            radius = 25
            rounded_rect_height = bubble_height - 25
            speech_bubble.create_polygon(
                radius, 0,
                bubble_width - radius, 0,
                bubble_width, radius,
                bubble_width, rounded_rect_height - radius,
                bubble_width - radius, rounded_rect_height,
                radius, rounded_rect_height,
                0, rounded_rect_height - radius,
                0, radius,
                fill="white", outline="white", width=2
            )

            # Define the triangle points
            triangle_points = [
                bubble_width / 2 - 25, bubble_height - 50,
                bubble_width / 2 + 25, bubble_height - 50,
                bubble_width / 2, bubble_height
            ]

            # Create the triangle
            speech_bubble.create_polygon(triangle_points, fill="white", outline="white", width=2)
            speech_bubble.pack()

            # Resize window to fit text on the screen
            speech_window.geometry(f"{bubble_width}x{bubble_height}+{int(speech_x)}+{int(speech_y)}")
            speech_window.update()

            # Create new top level window for text
            text_window = tk.Toplevel(speech_window)
            text_window.resizable(0, 0)
            # Remove close/minimize bar on the top
            text_window.overrideredirect(1)
            # make the text window always on top
            text_window.attributes("-topmost", True)

            # Create text box
            text_box = tk.Label(text_window, text="", width=bubble_width - 25, height=bubble_height - 25, bg="white", fg="black", font=("Arial", 12), highlightthickness=0, bd=0, wraplength=bubble_width - 20, justify="center", anchor="center")
            text_box.pack()
            # Resize window to fit text on the screen
            text_window.geometry(f"{bubble_width - 25}x{bubble_height - 50}+{int(speech_x + 12.5)}+{int(speech_y + 12.5)}")
            text_window.update()

            def type_text(i=0):
                if i < len(text):
                    text_box.config(text=text_box.cget("text") + text[i])
                    text_window.after(50, type_text, i + 1)  # Adjust the delay as needed

            type_text()

            # Destroy the window after a time proportional to the amount of words, and set isTalking to False
            speech_window.after(int(len(text.split()) * 500), lambda: (speech_window.destroy(), setattr(self, "isTalking", False)))

    def play_sound(self, filename):
        # Play the sound
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def stop_sound(self, event):
        pygame.mixer.music.stop()
            
