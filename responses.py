import os
import aiohttp
from dotenv import load_dotenv
from calendar_auth import get_three_days_events

load_dotenv() # Load environment variables from .env file
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


async def get_responses(user_input: str) -> str: # Function to get responses based on user input
    lowered = user_input.lower() # Convert user input to lowercase for case-insensitive matching

    if "hi" in lowered:
        return "Hello!"
    elif "weather" in lowered:
        return await fetch_weather("Turku")
    elif "calendar" in lowered:
        return get_three_days_events()
    else:
        return "I don't understand what you mean."
    
    
async def fetch_weather(city: str) -> str: # Function to fetch weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        async with aiohttp.ClientSession() as session: # Create an asynchronous session for making HTTP requests
            async with session.get(url) as response: 
                if response.status == 200:
                    data = await response.json() # Parse the JSON response
                    temperature = data["main"]["temp"] # Get the temperature
                    weather_description = data["weather"][0]["description"] # Get the weather description
                    return f"{city}: {temperature}°C with {weather_description}."
                else:
                    return "Could not fetch the weather data."
    except Exception as e:
        return e