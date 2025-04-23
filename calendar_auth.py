import os
import datetime
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # Define the scope for the Google Calendar API


def get_calendar_service(): # Create a service for the Google Calendar API
    creds = None # Initialize credentials to None

    # Check if token.pickle file exists to load saved credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid: # Check if credentials are valid
        if creds and creds.expired and creds.refresh_token: # If the credentials are expired, refresh them
            creds.refresh(Request())
    
        else: # If there are no valid credentials, prompt the user to log in
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token: # Save the credentials for the next run
            pickle.dump(creds, token)

        
    service = build('calendar', 'v3', credentials=creds) # Build the Google Calendar service

    return service


def get_three_days_events():
    service = get_calendar_service() # Get the calendar service

    # Get today's date
    today = datetime.date.today()
    start_of_three_days = datetime.datetime.combine(today, datetime.time.min).isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_three_days = datetime.datetime.combine(today + datetime.timedelta(days=2), datetime.time.max).isoformat() + 'Z'

    # Call the Calendar API to get today's events
    events_result = service.events().list(calendarId='primary', timeMin=start_of_three_days,
                                          timeMax=end_of_three_days, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return "No events found for today."
    
    response = "Next three days events:\n"
    for event in events:
        summary = event['summary']
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        color_id = event.get('colorId', 'default')
        
        # Extract the date and time
        start_day = start[:10] if "T" in start else start
        weekday = datetime.datetime.strptime(start_day, "%Y-%m-%d").strftime("%A")
        start_time = start[11:16] if "T" in start else start
        end_time = end[11:16] if "T" in end else end

        response += f"- {weekday}, {summary} from {start_time} to {end_time}\n"

    return response # Return the formatted response with today's events