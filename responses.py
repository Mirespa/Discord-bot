import os
import aiohttp
import random
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
    elif "steam" in lowered:
        return await get_steam_special_offers()
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


async def get_steam_special_offers() -> str: # Function to fetch Steam deals
    url = "https://store.steampowered.com/api/featuredcategories"

    try:
        async with aiohttp.ClientSession() as session: # Create an asynchronous session for making HTTP requests
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json() # Parse the JSON response
                    specials = data.get("specials", {}).get("items", [])

                    # Check if there are any specials available
                    if not specials:
                        return "No deals found."

                    # Get first 20 items from specials and select 5 randomly
                    top_20 = specials[:20]
                    selected_games = random.sample(top_20, min(5, len(top_20)))

                    # Create a response string with the selected games
                    response = "Steam Deals:\n"
                    for game in selected_games:
                        title = game.get("name")
                        discount = game.get("discount_percent", 0)
                        price = game.get("final_price", 0) / 100
                        old_price = game.get("original_price", 0) / 100
                        game_url = f"https://store.steampowered.com/app/{game.get('id')}"

                        response += f"{title} - {discount}% off! {price:.2f}€ (was {old_price:.2f}€)\n{game_url}\n\n" # Format the response string with game details
                    return response 
                else:
                    return f"Could not fetch the Steam deals (status code {resp.status})."
    except Exception as e:
        return e