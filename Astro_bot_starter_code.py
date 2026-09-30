# =========================
# REQUIRED LIBRARIES
# =========================
import requests
import json
import time

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ")
        return f"Bearer {token}"
    else:
        return "Bearer YOUR_WEBEX_TOKEN"
    
def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use hard-coded API key? (y/n): ").lower()
    if choice == "n":
        api_key = input(prompt)
        return api_key
    else:
        return hardcoded_key

# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching rooms:", response.status_code)
        return []

    return response.json().get("items", [])

def print_rooms(rooms):
    for room in rooms:
        print(f"- {room['title']} (ID: {room['id']})")

def select_room(rooms):
    while True:
        name = input("What is the room name? ")
        for room in rooms:
            if name.lower() in room["title"].lower():
                print(f"Successfully selected room: {room['title']}")
                return room["id"]
        print("Room not found, Please try again.")

def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None, None, None # Added third None

    data = response.json().get("items", [])
    if not data:
        return None, None, None # Added third None

    latest = data[0]
    return latest.get("id"), latest.get("text", ""), latest.get("personEmail", "")

def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token, 
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "text": str(message)
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")

# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data[0] if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None

def get_weather(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return {"error": "City not found or network error"}
        
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "units": "metric",
        "appid": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        weather = response.json()
        
        weather_list = weather.get("weather", [{}])
        description = weather_list[0].get("description") if weather_list else None
        
        return {
            "city": weather.get("name"),
            "country": weather.get("sys", {}).get("country"),
            "temperature": weather.get("main", {}).get("temp"),
            "description": description,
            "humidity": weather.get("main", {}).get("humidity"),
            "wind_speed": weather.get("wind", {}).get("speed")
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return {"error": "Failed to fetch weather data"}

# =========================
# MAIN BOT LOGIC
# =========================
def main():
    token = get_webex_token()
    rooms = get_rooms(token)

    weather_key = get_api_key("Weather API key", "a3799325cd079312f575d330710f98ef")

    if not rooms:
        print("No Webex rooms found. Please ensure your bot is added to a space.")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _, _ = get_latest_message(token, room_id)
    print("Bot is now listening for messages...")

    while True:
        message_id, message_text, sender_email = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:
            last_message_id = message_id
            
            if sender_email and sender_email.endswith("@webex.bot"):
                continue

            print(f"Received new message: {message_text}")

            slash_index = message_text.find("/")
            
            if slash_index == -1:
                continue

            command_string = message_text[slash_index:].strip()
            parts = command_string.split(maxsplit=1)
            command = parts[0].lower()

            if command == "/help":
                send_message(
                    token,
                    room_id,
                    "Available commands:\n- /hello\n- /help\n- /quit\n- /weather <city>"
                )
            elif command == "/hello":
                send_message(token, room_id, "Hello! I am receiving your messages loud and clear.")

            elif command == "/weather":
                if len(parts) > 1:
                    city = parts[1]
                    weather_data = get_weather(city, weather_key)
                    
                    if "error" in weather_data:
                        msg = weather_data["error"]
                    else:
                        msg = (f"Weather in {weather_data['city']}, {weather_data['country']}: "
                               f"{weather_data['temperature']}°C, {weather_data['description']}. "
                               f"Humidity: {weather_data['humidity']}%, Wind: {weather_data['wind_speed']} m/s.")
                        
                    send_message(token, room_id, msg)
                else:
                    send_message(token, room_id, "Please specify a city. Usage: /weather <city>")

            elif command == "/quit":
                send_message(token, room_id, "Bot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help to see available commands.")

        time.sleep(5)

if __name__ == '__main__':
    main()