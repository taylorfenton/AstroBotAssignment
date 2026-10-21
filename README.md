# 🚀 Space Bot API Investigation Sheet

**Total Marks: 40**  
**TASK 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, **Weather API** and a **Geocoding API** , plus the Python time module. Also furhter investigate the application of Web Architecture and MVC design pattern in development of the Bot

---

##  Webex Messaging API (4 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1/rooms` |
| Authentication Method | `API Key` |
| Endpoint to list rooms | `GET /rooms` |
| Endpoint to get messages | `GET /messages?roomId={roomId}&max=1` |
| Endpoint to send message | `POST /messages` |
| Required headers | `"Authorization": "Bearer {token}", "Content-Type": "application/json"` |
| Sample full GET or POST request | `requests.post("[https://webexapis.com/v1/messages](https://webexapis.com/v1/messages)", headers={"Authorization": token, "Content-Type": "application/json"}, data=json.dumps({"roomId": room_id, "text": message}))` |

---

##  ISS Current Location API (2 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `/iss-now.json` |
| Sample response format | `"message": "success", "timestamp": 1791363823, "iss_position": {"longitude": "150.7680", "latitude": "-22.6111" ` | 

---

##  Geocoding API (4 marks)

| Criteria | Details |
|---------|---------|
| Provider used (Choose one) | **LocationIQ / Mapbox/ OpenWeatherMap other -provide detail** |
| API Base URL | `http://api.openweathermap.org/geo/1.0/direct` |
| Endpoint for geocoding | `direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}` |
| Endpoint for reverse geocoding | `reverse?lat={lat}&lon={lon}&limit={limit}&appid={API key}` |
| Authentication method | `API Key passed as appid query parameter` |
| Required query parameters | `q, appid, limit` |
| Sample request with latitude/longitude | `http://api.openweathermap.org/geo/1.0/reverse?lat=51.5098&lon=-0.1180&limit=5&appid={API key}` |
| Sample JSON response (formatted example) | `"name":"City of Westminster","local_names":{"be":"Вэстмінстэр","ru":"Вестминстер","fr":"Cité de Westminster","cy":"San Steffan","ko":"시티오브웨스트민스터","he":"וסטמינסטר","en":"City of Westminster","mk":"Град Вестминстер"},"lat":51.4973206,"lon":-0.137149,"country":"GB","state":"England" ` | 

---


##  Weather API (3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | 'OpenWeather' |
| API Base URL | `https://api.openweathermap.org/geo/1.0/direct` |
| Endpoint for current weather | `weather` |
| Authentication method | `API Key passed in via appId` |
| Required query parameters | `lat, lon, appid, units` |
| Sample JSON response (formatted example) | `"weather": [{"description": "clear sky"}], "main": {"temp": 22.5, "humidity": 45}, "wind": {"speed": 3.1}, "sys": {"country": "GB"}, "name": "London"` | 

---

##  Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `datetime` |
| Function used to convert epoch | `.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')` | 
| Sample code to convert timestamp | `import time - print(usable_time(timestamp))` | 
| Output (human-readable time) | `Fri Sept 18 11:00:19 2026` |

---

##  Extended Feature API V1 ( 3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | 'uselessfacts' |
| API Base URL | `https://uselessfacts.jsph.pl` |
| Endpoint | `api/v2/facts/random` |
| Authentication method | `Json, no key` |
| Required query parameters | `none` |
| Sample JSON response (formatted example) | `"id":"6edb5c2eb67ca5a7b00eedb270804dbf","text":"Like fingerprints, everyone's tongue print is different!","source":"djtech.net","source_url":"https://www.djtech.net/humor/shorty_useless_facts.htm","language":"en","permalink":"https://uselessfacts.jsph.pl/api/v2/facts/6edb5c2eb67ca5a7b00eedb270804dbf"` | 

--- 

##  Extended Feature API V2 ( 3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | ' NASA ' |
| API Base URL | `https://api.nasa.gov/` |
| Endpoint | `planetary/apod` |
| Authentication method | `API Key` |
| Required query parameters | `hdurl, explanation` |
| Sample JSON response (formatted example) | `"date":"2026-10-07","explanation":"\"Happy New Year!\" No, wait, this is not a fireworks display. This image shows Nebula Pa 30, observed with the Gemini North Telescope in Hawai'i. It is likely the remnant of an old supernova explosion: separate historical records by Chinese, Japanese and Arabic astronomers tell of a \"guest star\" that appeared in the sky for 185 days in the year 1181. It is believed that this bright new point of light came from the supernova that caused the fireworks in Pa 30. Astronomers don't know exactly what happened in this unusual explosion, classified as a Type Iax supernova, but it is thought to be caused by the merger of two white dwarfs. The mysterious central star in the image is extremely hot and produces a strong wind, possibly forming the radial filaments. Look closely at them: those pearl-like knots stringing the filaments are 4 light-days in diameter. Understanding how a supernova created this amazing nebula continues an 845-year old mystery (and counting).Tomorrow's picture: sm\u00f6rg\u00e5sbord\t\t\t\t\t\t","hdurl":"https://science.nasa.gov/wp-content/themes/nasa-child/assets/images/nasa-logo@2x.png","media_type":"image","service_version":"v1","title":"NASA Science","url":"https://science.nasa.gov/wp-content/themes/nasa-child/assets/images/nasa-logo@2x.png"` | 

--- 

##  Evaluation – Web Architecture, MVC Design & Security 

In this section, evaluate how web technologies, architecture, and design patterns have been applied in your **AstroBot**. Your responses must relate directly to your implementation and include reflection on your design decisions.

---

###  Web Architecture – Client–Server Model (3 marks)

Explain how the client–server model applies to your AstroBot:

- Identify the **client**:

The Python script acts as the primary client. The end-user's Webex application also acts as a client interfacing with the Webex servers.

- Identify the **server(s)**

The servers include the Webex API servers, OpenWeatherMap servers, Open-Notify (ISS) servers, uselessfacts.jsph.pl, and NASA's Science API servers.

- Describe how data flows between:
  - User, AstroBot and APIs

1. First the user enters a command (e.g., `/weather <city>`)
2. Program (Client) polls the WebexAPI to get the latest message
3. The bot processes the command given, and goes at fetches the data from the relevant API. In this case, the OpenWeather API.
4. Weather API respoonds with JSON data to the bot.
5. Bot formats given data and then sends a `POST` request back the WebexAPI which then delivers the data in human-readable form on the messeaging client.

**Simple block diagram here**

####  Security Considerations: (3 marks )
- **API Keys and Tokens:** The bot uses prompts via `input()` to allow users to inject their Webex tokens and API keys at runtime, instead of hardcoding them directly into the script.

- **API Rate Limiting:** To prevent spamming the Webex API and encountering rate limits, the bot loop includes a `sleep()` delay between request attempts.

- **Input Validation:** The bot splits command strings using parts = command_string.split(maxsplit=1) and validates array lengths (e.g., `if len(parts) > 1:`) before attempting to process user arguments like city names. This gives an easy way to look at each section of the users command and act accordingly.
---

###  RESTful API Usage in Your Application (3 marks )

- **HTTP Methods:** The bot mostly uses GET requests to retrieve information, such as fetching Webex rooms, polling for messages, and requesting external data from the Weather, ISS, and other APIs. POST requests are strictly used to create resources, specifically sending new messages to Webex rooms.

- **API Interaction:** The bot passes authentication either via headers (e.g., `"Authorization":` token for Webex) or via query parameters (e.g., `"appid"`: api_key for OpenWeather). 

- **JSON Processing:** The application parses incoming JSON packages using the `response.json()` method. To safely navigate nested data structures and prevent error exceptions when fields are missing, the bot relies on the dictionary `.get()` method, seen when extracting temperature data via `weather.get("main", {}).get("temp")`. 


#### Security Considerations: (2 marks)
- **Response Status Codes:** The application continuously validates API responses by checking if `response.status_code != 200:` and using `response.raise_for_status()` to catch HTTP errors.

---

###  MVC Design Pattern in AstroBot (3 Marks)

| Component   | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model**  | Description: Handles data logic, retrieval, and structuring. <br> <br> Example: Functions like get_weather(), get_iss_location(), and get_apod() act as the Model. They encapsulate the logic for fetching data from the APIs and returning dictionaries/lists without caring how it will be displayed. |
| **View**   | Description: Represents user interface and how data is presented. <br> <br> Example: In this chat application, the Webex messaging interface is the View. The bot prepares the View by formatting data into human-readable text `(e.g., msg = f"Astronomy Picture of the Day\nTitle: {apod['title']}...")` before sending it to the user. |
| **Controller** | Description: Dictates the flow between the user, View, and Model. <br> <br> Example: The `main()` function is the Controller. It monitors for user inputs (messages), parses the commands (e.g., `elif command == "/weather":`), calls the relevant function (`get_weather()`), and then passes the result back to the View via `send_message()`. |

---

### 📝 Reflection and Evaluation ( 8 marks )

Reflect on your AstroBot (400 words):

 The bots effectivness achieves exactly what it was tasked to do, giving structured responeses for each API including Messaging, Weather, ISS Location and Geocoding/Reverse Geocoding. A user can connect to the bot via the python script using thier own keys and input a valid command, each connecting to their respective API. The script then fetches the correct data, and outputs it for the user in an easily readable format. 
 <br></br>
 One decision I thought was impactful during development was having a clear structure when coding. Seperating each API's function into it's own lot of subroutines combined with clear commenting helped keep me on track rather than being confused on where I was and loosing focus. Another decision I found went well was packing together both geocoding styles into one command `/locate`. For the user, this eliminates another command to remember whilst also logically bunching relevant processes together (e.g: `/locate` can have two inputs, a City or coordiantes, if it sees coordinates, it will output a city/sea and vice versa if coordinates are entered.).
 <br></br>
 When introducing one of my extra API's, one of them returned an image (APOD API). This posed a problem because my current `send_message`  subroutine couldn't output an image link. This involved me looking at webex's forums finding a way to return message with an image attached and, after mutliple tries I was able to find that it can also parse a files parameter. A bit more configuring and I got it to send the Picture of the day from Nasa's Astronomy API. Also, another big issues was that the bot was responding to its own messages (e.g: The user typed `/help`, it would display the list of commands available, then it would go to execute any commands it could find within its own message). The way I managed to fix this was to exclude any responses where the email ended with `@webex.bot`, meaning it then only read messages other than itself. None of my commands also require another response after the inital message so no further action was needed.
 <br></br>
 One major security risk with any API programs is keys, and more importantly, keys being leaked online. This can be a huge risk financially as some API's will start to charge if you go over their rate limit (e.g. 1000 requests a day). Because of this, before releasing this repo to the public, I have gone and removed all hard-coded keys within the program. This stops anyone having access the keys and abusing them. Being aware of this, for my extended feature, I opted more for API's that didn't require an account and therefore another key.
  <br></br>
  To improve my design, I think starting from scracth rather than following some starter code would've helped me understand the program more interms of how its layed out and the different functions that went into the program faster, allowing more time for futher development. Another way I could've improved my program would be to use a different messaging service, as with webex, I encounted many minor problems that kept on stacking up eventually leading to bigger issues down the road.


---

 **Tip:** Link your answers directly to your code and examples for higher marks.
### Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

###  Total: /40