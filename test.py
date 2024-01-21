import tkinter as tk
import subprocess

is_duck_enabled = False
pet_manager_process = None  # Initialize pet_manager_process in the global scope

def toggle_duck():
    global pet_manager_process, is_duck_enabled

    if is_duck_enabled:
        if pet_manager_process:
            pet_manager_process.terminate()
            pet_manager_process = None
        is_duck_enabled = False
    else:
        pet_manager_process = subprocess.Popen(["python3", "pet_manager.py"])
        is_duck_enabled = True

def enableDuck():
    global pet_manager_process
    pet_manager_process = subprocess.Popen(["python3", "pet_manager.py"])

def disableDuck():
    global pet_manager_process
    if pet_manager_process:
        pet_manager_process.terminate()



while True:
    bob = input("Enter something: ")
    if bob == "quit":
        disableDuck()
        break
    elif bob == "enable":
        enableDuck()
    else:
        print("You entered", bob)
