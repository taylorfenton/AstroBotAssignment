# =========================
# REQUIRED LIBRARIES
# =========================
import requests     # Here lists all the required libraries used within the project
import json
import time
from datetime import datetime

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()   # Used to get Wexex token from user or use hard-coded token
    if choice == "n":
        token = input("Enter your Webex Access Token: ")
        return f"Bearer {token}"
    else:
        return "Bearer YOUR_WEBEX_TOKEN"
    
def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use hard-coded API key? (y/n): ").lower()  # Used to get the API key from user or use hard-coded key
    if choice == "n":
        api_key = input(prompt)
        return api_key
    else:
        return hardcoded_key

# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"      # API endpoint to get rooms
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching rooms:", response.status_code)    # If failure, catch error and return empty list
        return []

    return response.json().get("items", [])     # Return list of rooms

def print_rooms(rooms):     # Function to print the list of rooms
    for room in rooms:
        print(f"- {room['title']} (ID: {room['id']})")

def select_room(rooms):     # Function to select a room from the list
    while True:
        name = input("What is the room name? ")
        for room in rooms:
            if name.lower() in room["title"].lower():
                print(f"Successfully selected room: {room['title']}")
                return room["id"]
        print("Room not found, Please try again.")

def get_latest_message(token, room_id):     # Function to get the latest message from a room
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}      # Uses token from previous function

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:     # Catch any unexpected errors
        return None, None, None 

    data = response.json().get("items", [])
    if not data:
        return None, None, None 

    latest = data[0]
    return latest.get("id"), latest.get("text", ""), latest.get("personEmail", "")      # Return latest message details

def send_message(token, room_id, message):      # Function to send a message to a room
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token, 
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,      # Parameters that identify the room and message content
        "text": str(message)
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))   # Send the message

    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")      # Catch any errors then output them

def send_message_files(token, room_id, message, file_url):      # Function to send a message with a file to a room
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token, 
        "Content-Type": "application/json"
    }
    data = {                    # Parameters that identify the room and message content
        "roomId": room_id,
        "text": str(message),
        "files" : [file_url]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")      # Catch any errors then output them

# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):                        # Gets city coordinates from OpenWeatherMap API
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)     # Try to send a request to get data from API, otherwise catch errors
        response.raise_for_status()
        
        data = response.json()
        return data[0] if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None

def get_weather(city, api_key):                                 # Function to get weather information for a city
    location = get_city_coordinates(city, api_key)

    if not location:
        return {"error": "City not found or network error"}     # Handle case where city is not found

    url = "https://api.openweathermap.org/data/2.5/weather"     # API endpoint for current weather
    params = {
        "lat": location["lat"],     # Shows the latitude and longitude of the city to get the weather information
        "lon": location["lon"],
        "units": "metric",
        "appid": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)     # Try to send a request to get data from API, otherwise catch errors
        response.raise_for_status()
        
        weather = response.json()
        
        weather_list = weather.get("weather", [{}])
        description = weather_list[0].get("description") if weather_list else None
        
        return {
            "city": weather.get("name"),
            "country": weather.get("sys", {}).get("country"),       # Return all relevant weather information
            "temperature": weather.get("main", {}).get("temp"),
            "description": description,
            "humidity": weather.get("main", {}).get("humidity"),
            "wind_speed": weather.get("wind", {}).get("speed")
        }

    except requests.exceptions.RequestException as e:       # Catch any errors then output them
        print(f"Error fetching weather: {e}")
        return {"error": "Failed to fetch weather data"}
    
# =========================
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):                     # Takes latitude and longitude and returns the nearest city
    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)     # Try to send a request to get data from API, otherwise catch errors
        response.raise_for_status()
        
        data = response.json()
        
        return data[0] if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reverse geocode: {e}")
        return None

def get_iss_location(api_key):                          # Function to get the current location of the ISS, returns coordinates and location name
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]
    timestamp = data["timestamp"]
    usable_time = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')      # Format timestamp to human-readable
    location = reverse_geocode(lat, lon, api_key)
    place = "Over Ocean / No Nearby City"
    if location:
        place = location.get("name", "Unknown")
    return (
        lat,
        lon,
        place,
        usable_time
    )

# =========================
# Extended API FUNCTIONS
# =========================
def get_random_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"        # API endpoint for random facts

    try:
        response = requests.get(url, timeout=10)        # Try to send a request to get data from API, otherwise catch errors
        response.raise_for_status()
        
        data = response.json()
        return data if data else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random fact: {e}")
        return None

def get_apod():     # Get Astronomy Picture of the Day
    date_string = datetime.now().strftime("%d-%m-%Y")   # Get current date in dd-mm-yyyy format

    url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/"
    params = {
        "data": date_string
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)     # Try to send a request to get data from API, otherwise catch errors
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
    token = get_webex_token()       # Get any relevant tokens
    rooms = get_rooms(token)

    weather_key = get_api_key("Weather API key", "a3799325cd079312f575d330710f98ef")   

    if not rooms:
        print("No Webex rooms found. Please ensure your bot is added to a space.")      # Check if rooms are available
        return

    print_rooms(rooms)      # Display available rooms
    room_id = select_room(rooms)        # Select a room to listen for messages

    last_message_id, _, _ = get_latest_message(token, room_id)      # Get the latest message ID
    print("Bot is now listening for messages...")

    while True:     # Listen for new messages
        message_id, message_text, sender_email = get_latest_message(token, room_id)     # Get the latest message

        if message_id and message_id != last_message_id:        # Check if the message is new
            last_message_id = message_id

            if sender_email and sender_email.endswith("@webex.bot"):        # Ignore messages from the bot itself
                continue

            print(f"Received new message: {message_text}")      # Log the received message

            slash_index = message_text.find("/")        # Find the start of the command

            if slash_index == -1:
                continue

            command_string = message_text[slash_index:].strip()     # Extract command string
            parts = command_string.split(maxsplit=1)        # Split command and arguments
            command = parts[0].lower()      # Normalize command to lowercase

            if command == "/help":      # Display available commands
                send_message(
                    token,
                    room_id,
                    "Available commands:\n- /hello\n- /help\n- /quit\n- /weather <city>\n- /locate <city> OR <lat> <lon>\n- /iss\n- /apod"
                )
            elif command == "/hello":       # Respond to hello command, test if bot replies
                send_message(token, room_id, "Hello! I am receiving your messages loud and clear.")

            elif command == "/weather":     # Respond to weather command, returns weather information
                if len(parts) > 1:      # Check if a city was provided
                    city = parts[1]
                    weather_data = get_weather(city, weather_key)
                    
                    if "error" in weather_data:
                        msg = weather_data["error"]
                    else:
                        msg = (f"Weather in {weather_data['city']}, {weather_data['country']}: "
                               f"{weather_data['temperature']}°C, {weather_data['description']}. "
                               f"Humidity: {weather_data['humidity']}%, Wind: {weather_data['wind_speed']} m/s.")

                    send_message(token, room_id, msg)       # Send weather information
                else:
                    send_message(token, room_id, "Please specify a city. Usage: /weather <city>")   # Provide usage instructions

            elif command == "/iss":     # Respond to ISS location command, output coordinates and place
                iss_location = get_iss_location(weather_key)
                if iss_location:
                    lat, lon, place, usable_time = iss_location
                    msg = (f"Current ISS Location:\n"
                           f"Latitude: {lat}\n"
                           f"Longitude: {lon}\n"
                           f"Place: {place}\n"
                           f"Time: {usable_time}")
                else:
                    msg = "Could not retrieve ISS location."

                send_message(token, room_id, msg)

            elif command == "/locate":      # Either take in coordinates or a city name, and output its opposite
                if len(parts) > 1:      # Check if a query was provided
                    query = parts[1].strip()        # Get the query
                    query_parts = query.split()     # Split the query into parts

                    is_coords = False
                    if len(query_parts) == 2:       # Check if two parts were provided
                        try:
                            lat = float(query_parts[0])     # Get latitude
                            lon = float(query_parts[1])      # Get longitude
                            is_coords = True
                        except ValueError:
                            pass

                    if is_coords:       # If coordinates were provided
                        location = reverse_geocode(lat, lon, weather_key)   # Reverse geocode the coordinates
                        if location:        # If a location was found
                            state = f", {location['state']}" if "state" in location else ""                 # Get state and output details in message
                            country = location.get("country", "")
                            msg = f"The location for {lat}, {lon} is {location['name']}{state}, {country}."
                        else:
                            msg = f"Could not find a place for coordinates {lat}, {lon} (might be over the ocean)."  # If no location was found, output error message or over ocean
                    else:
                        location = get_city_coordinates(query, weather_key)     # Else try to get city coordinates, assume user has then entered a place name
                        if location:
                            state = f", {location['state']}" if "state" in location else ""     #Try to get and output coords
                            country = location.get("country", "")
                            msg = (f"Coordinates for {location['name']}{state}, {country}:\n"
                                   f"Latitude: {location['lat']}\n"
                                   f"Longitude: {location['lon']}")
                        else:
                            msg = f"Could not find coordinates for '{query}'."
                            
                    send_message(token, room_id, msg)
                else:
                    send_message(token, room_id, "Usage: /locate <city> OR /locate <lat> <lon>")

            elif command == "/fact":        # Output random fact
                fact = get_random_fact()
                if fact:
                    send_message(token, room_id, f"Random Fact: {fact['text']}")        #Try send message or catch for any errors
                else:
                    send_message(token, room_id, "Could not retrieve a random fact.")

            elif command == "/apod":        # Get Astronomy Picture of the Day, using different send message function due to sending pictures as well as text
                apod = get_apod()
                if apod:
                    msg = (f"Astronomy Picture of the Day\n"
                           f"Title: {apod['title']}\n"
                           f"Date: {apod['date']}\n"
                        )
                else:
                    msg = "Could not retrieve Astronomy Picture of the Day."

                send_message_files(token, room_id, msg, apod['hdurl'] if apod else None)

            elif command == "/quit":                                # Exit loop to stop bot
                send_message(token, room_id, "Bot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help to see available commands.")       # If command is not recognized, output error message

        time.sleep(5)

if __name__ == '__main__':
    main()