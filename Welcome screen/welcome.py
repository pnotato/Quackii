import tkinter as tk
import subprocess

# Global variable to keep track of the process
pet_manager_process = None

def run_pet_manager():
    global pet_manager_process
    # Start the pet_manager.py and keep a reference to the process
    pet_manager_process = subprocess.Popen(["python", "Pet Manager/pet_manager.py"])

def stop_pet_manager():
    global pet_manager_process
    if pet_manager_process:
        # Terminate the process
        pet_manager_process.terminate()
        pet_manager_process = None

# Create the main window
root = tk.Tk()
root.title("Virtual Duck Assistant")

# Set the window size and position
root.geometry("400x300+300+300")

# Add a welcome message
welcome_label = tk.Label(root, text="Welcome to the Virtual Duck Assistant!", font=("Arial", 14))
welcome_label.pack(pady=20)

# Add a button to start the virtual assistant
start_button = tk.Button(root, text="Enable Duck", command=run_pet_manager)
start_button.pack(pady=10)

# Add a button to stop the virtual assistant
stop_button = tk.Button(root, text="Disable Duck", command=stop_pet_manager)
stop_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()