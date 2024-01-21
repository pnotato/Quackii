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
        button = request.form.get('button')
        if button == 'back':
            return redirect("/")

        reminder_name = request.form['reminderName']
        reminder__start_date = request.form['reminderStartDate']
        reminder__end_date = request.form['reminderEndDate']
        reminder_start_time = request.form['reminderStartTime']
        reminder_end_time = request.form['reminderEndTime']
        reminder_location = request.form['reminderLocation']

        # Parse the date and time into the required format (start and end times/dates included)
        reminder__start_date = reminder__start_date.split('-')
        reminder__end_date = reminder__end_date.split('-')
        reminder_start_time = reminder_start_time.split(':')
        reminder_end_time = reminder_end_time.split(':')
        reminder__start_date = {"year": int(reminder__start_date[0]), "month": int(reminder__start_date[1]), "day": int(reminder__start_date[2])}
        reminder__end_date = {"year": int(reminder__end_date[0]), "month": int(reminder__end_date[1]), "day": int(reminder__end_date[2])}
        reminder_start_time = {"hour": int(reminder_start_time[0]), "minute": int(reminder_start_time[1])}
        reminder_end_time = {"hour": int(reminder_end_time[0]), "minute": int(reminder_end_time[1])}

        reminder_start = {"year": reminder__start_date["year"], "month": reminder__start_date["month"], "day": reminder__start_date["day"], "hour": reminder_start_time["hour"], "minute": reminder_start_time["minute"]}
        reminder_end = {"year": reminder__end_date["year"], "month": reminder__end_date["month"], "day": reminder__end_date["day"], "hour": reminder_end_time["hour"], "minute": reminder_end_time["minute"]}

        print(reminder_name, reminder_start, reminder_end, reminder_location)

        # Create a new reminder
        reminders_instance = Reminders()
        reminders_instance.create_event(reminder_name, reminder_start, reminder_end, reminder_location)
        # Redirect to the same page to refresh the reminders list
        return redirect("/reminders")
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
    
