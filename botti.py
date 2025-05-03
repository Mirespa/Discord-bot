import os
from discord import Intents, Client, Message
from dotenv import load_dotenv 
from responses import get_responses

load_dotenv() # Load environment variables from .env file
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.default() # Create default intents for the bot
intents.message_content = True # Enable message content intents

client = Client(intents=intents) # Create a client instance with the specified intents


async def send_response(message: Message) -> None: # Function to send a response
    try:
        response: str = await get_responses(message.content) # Get the response based on the message content
        await message.channel.send(response) # Send the response
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None: # Function to run when the bot is ready
    print(f'{client.user} is running') # Print the bot's username to the console


@client.event
async def on_message(message: Message) -> None: # Function to handle incoming messages
    if message.author == client.user: # Ignore messages from the bot itself
        return
    
    # Debugging information
    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)
    print(f"{username} in {channel}: {user_message}") # Print the message details to the console

    await send_response(message) # Call the send_response function to handle the message


def main() -> None:
    client.run(DISCORD_TOKEN) # Start the bot with the token from the environment variable


if __name__ == "__main__": 
    main() # Call the main function to run the bot