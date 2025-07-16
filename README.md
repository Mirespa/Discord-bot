# Discord Bot

"Personal assistant" style discord bot 
It supports modular logic, responds to user messages, and includes optional integration with services like Google Calendar and weather APIs.

## Features
- Responds to text messages in Discord channels
- Custom response logic via `responses.py`
- Fetches daily Steam game deals
- Secure token management using `.env`
- Google Calendar integration (`calendar_auth.py`)
- Weather command support using an external API (e.g., OpenWeatherMap)

## Educational Value
- How to build and structure a Python-based Discord bot
- Using async I/O (async / await) in Python
- Safely manage secrets and API keys with environment variables
- Building modular and testable code
- Integrate 3rd-party APIs like Google Calendar & OpenWeatherMap

## How to run
1. Install requirements
```
pip install -U discord.py python-dotenv requests google-api-python-client google-auth google-auth-oauthlib
```

2. Set up environment variables
Create a `.env` file in the root directory and add:
```
DISCORD_TOKEN=
WEATHER_API_KEY=
```

3. Run the bot
```
python botti.py
```
