from flask import Flask, render_template, request, redirect, url_for
import tkinter as tk
import subprocess
from Calendar.reminder import Reminders
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
        if is_duck_enabled:
            currentstate = "DISABLE THE DUCK!"
        else:
            currentstate = "SUMMON THE DUCK!"
        return render_template('index.html', currentstate=currentstate)
    
@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        return redirect("/")
        # button = request.form.get('button')
        # if button == 'home':
        #     return redirect("/")
        
        # username = request.form['username']
        # status = request.form['status']

        # # write these to a file
        # with open("settings.txt", "w") as f:
        #     f.write(username + "\n")
        #     f.write(status + "\n")
        
    else: 
        return render_template('settings.html')
    
@app.route("/reminders", methods=['GET', 'POST'])
def reminders(): 
    if request.method == 'POST':
        return redirect("/settings")
    else:
        reminders_instance = Reminders()
        reminders_list = reminders_instance.read_events(10)  # Adjust the number as needed
        return render_template('reminders.html', reminders=reminders_list)

@app.route("/history", methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        return redirect("/")
    else: 
        return render_template('history.html')

@app.route("/credits", methods=['GET', 'POST'])
def credits():
    if request.method == 'POST':
        return redirect("/")
    else: 
        return render_template('credits.html')

@app.route("/API", methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        return redirect("/settings")
    else: 
        return render_template('apis.html')
    
@app.route("/messages", methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        print(f"Name: {name}, Message: {message}")
        return redirect("/")
    else: 
        return render_template('messages.html')
    
