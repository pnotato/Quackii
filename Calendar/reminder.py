import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class Reminders:
    
    def __init__(self):
        self.creds = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json")

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    # name is a string
    # startime and endtime are dictionaries with keys "year", "month", "day", "hour", "minute"
    # location is a string
    def create_event(self, name, starttime, endtime, location):
        self.authenticate()  # Ensure authentication before creating an event
        try:
            service = build("calendar", "v3", credentials=self.creds)
            event = {
                "summary": name,
                "location": location,
                "description": "This event was created by ducky!",
                "colorId": 5, # makes it ducky coloured!
                "start": {
                    "dateTime": dt.datetime(starttime["year"], starttime["month"], 
                                            starttime["day"], starttime["hour"], starttime["minute"], 0).isoformat(),
                    "timeZone": "America/Vancouver"
                },
                "end": {
                    "dateTime": dt.datetime(endtime["year"], endtime["month"],
                                            endtime["day"], endtime["hour"], endtime["minute"], 0).isoformat(),
                    "timeZone": "America/Vancouver"
                },
                "recurrence": [
                    "RRULE:FREQ=DAILY;COUNT=1"
                ]
            }

            event = service.events().insert(calendarId="primary", body=event).execute()

            print(f"Event created {event.get('htmlLink')}")

        except HttpError as error:
            print("An error occurred:", error)

    # amount is an integer that reads the previous amount of events
    def read_events(self, amount):
        self.authenticate()  # Ensure authentication before reading events
        try:
            service = build("calendar", "v3", credentials=self.creds)
        
            now = dt.datetime.utcnow().isoformat() + "Z"

            events_result = (
                service.events().list(
                    calendarId="primary",  # current calendar
                    timeMin=now,  # earliest we're interested in
                    maxResults=amount,  # number of upcoming events
                    singleEvents=True,
                    orderBy="startTime"
                ).execute()
            )
            events = events_result.get("items", [])
            if not events:
                return ["No upcoming events found."]

            total_events = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                total_events.append([start, event["summary"]])

            return total_events

        except HttpError as error:
            return("An error occurred:", error)

# Example usage:
reminders_instance = Reminders()
print(reminders_instance.create_event("Quack Quack", 
                                      {"year": 2024, "month": 1, "day": 20, "hour": 10, "minute": 0}, 
                                      {"year": 2024, "month": 1, "day": 20, "hour": 12, "minute": 0},
                                      "Test Location"))
