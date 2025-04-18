def get_responses(user_input: str) -> str:
    lowered = user_input.lower() # Convert user input to lowercase for case-insensitive matching

    if "hi" in lowered:
        return "Hello!"
    else:
        return "I don't understand what you mean."