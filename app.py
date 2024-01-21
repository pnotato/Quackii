from flask import Flask, render_template, request, redirect, url_for
import tkinter as tk
import subprocess

is_duck_enabled = False
pet_manager_process = None  # Initialize pet_manager_process in the global scope

def toggle_duck():
    global pet_manager_process, is_duck_enabled

    if is_duck_enabled:
        disableDuck()
        is_duck_enabled = False
    else:
        enableDuck()
        is_duck_enabled = True

def enableDuck():
    global pet_manager_process
    pet_manager_process = subprocess.Popen(["python3", "pet_manager.py"])

def disableDuck():
    global pet_manager_process
    if pet_manager_process:
        pet_manager_process.terminate()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        toggle_duck()
        return redirect("/")
    else: 
        return render_template('index.html')
    

