# =========================
# REQUIRED LIBRARIES
# =========================
import requests
import json
import time
from datetime import datetime

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
        return None, None, None 

    data = response.json().get("items", [])
    if not data:
        return None, None, None 

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

def send_message_files(token, room_id, message, file_url):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token, 
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "text": str(message),
        "files" : [file_url]
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
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):
    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return data[0] if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reverse geocode: {e}")
        return None

def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]
    location = reverse_geocode(lat, lon, api_key)
    place = "Over Ocean / No Nearby City"
    if location:
        place = location.get("name", "Unknown")
    return (
        lat,
        lon,
        place
    )

# =========================
# Extended API FUNCTIONS
# =========================
def get_random_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random fact: {e}")
        return None

def get_apod():
    date_string = datetime.now().strftime("%Y-%m-%d")

    url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/"
    params = {
        "data": date_string
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data[0] if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Astronomy Picture of the Day: {e}")
        return None
# =========================
# MAIN BOT LOGIC
# =========================
def main():
    token = get_webex_token()
    rooms = get_rooms(token)

    weather_key = get_api_key("Weather API key", "a3799325cd079312f575d330710f98ef")
    nasa_key = get_api_key("NASA API key", "TSrLl9s28LPL4I5Qs0hN4WH9ksGdooIiW1HaansC")

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
                    "Available commands:\n- /hello\n- /help\n- /quit\n- /weather <city>\n- /locate <city> OR <lat> <lon>\n- /iss"
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
            
            elif command == "/iss":
                iss_location = get_iss_location(weather_key)
                if iss_location:
                    lat, lon, place = iss_location
                    msg = (f"Current ISS Location:\n"
                           f"Latitude: {lat}\n"
                           f"Longitude: {lon}\n"
                           f"Place: {place}")
                else:
                    msg = "Could not retrieve ISS location."

                send_message(token, room_id, msg)

            elif command == "/locate":
                if len(parts) > 1:
                    query = parts[1].strip()
                    query_parts = query.split()
                    
                    is_coords = False
                    if len(query_parts) == 2:
                        try:
                            lat = float(query_parts[0])
                            lon = float(query_parts[1])
                            is_coords = True
                        except ValueError:
                            pass
                    
                    if is_coords:
                        location = reverse_geocode(lat, lon, weather_key)
                        if location:
                            state = f", {location['state']}" if "state" in location else ""
                            country = location.get("country", "")
                            msg = f"The location for {lat}, {lon} is {location['name']}{state}, {country}."
                        else:
                            msg = f"Could not find a place for coordinates {lat}, {lon} (might be over the ocean)."
                    else:
                        location = get_city_coordinates(query, weather_key)
                        if location:
                            state = f", {location['state']}" if "state" in location else ""
                            country = location.get("country", "")
                            msg = (f"Coordinates for {location['name']}{state}, {country}:\n"
                                   f"Latitude: {location['lat']}\n"
                                   f"Longitude: {location['lon']}")
                        else:
                            msg = f"Could not find coordinates for '{query}'."
                            
                    send_message(token, room_id, msg)
                else:
                    send_message(token, room_id, "Usage: /locate <city> OR /locate <lat> <lon>")

            elif command == "/fact":
                fact = get_random_fact()
                if fact:
                    send_message(token, room_id, f"Random Fact: {fact['text']}")
                else:
                    send_message(token, room_id, "Could not retrieve a random fact.")
            
            elif command == "/apod":
                apod = get_apod()
                if apod:
                    msg = (f"**Astronomy Picture of the Day**\n"
                           f"Title: {apod['title']}\n"
                           f"Date: {apod['date']}\n"
                        )
                else:
                    msg = "Could not retrieve Astronomy Picture of the Day."

                send_message_files(token, room_id, msg, apod['hdurl'] if apod else None)

            elif command == "/quit":
                send_message(token, room_id, "Bot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help to see available commands.")

        time.sleep(5)

if __name__ == '__main__':
    main()