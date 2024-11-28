## AVA: The Anime-Inspired Virtual Assistant

AVA (Autonomous Virtual Assistant) is an anime waifu virtual assistant. It leverages advanced AI technologies, including Google GenAI and Character AI, to provide intelligent and interactive responses. AVA can handle tasks such as opening applications, fetching weather updates, running speed tests, and more—all without relying on any external app for its GUI. This self-contained virtual assistant offers a seamless and charming experience inspired by anime characters.

<p align="center">
<a href="https://github.com/Ronen6999/Autonomous-Virtual-Assistant">
    <img src="https://i.ibb.co/2hT7Hgm/2024-05-20-2.png" alt="Autonomous Virtual Assistant">
</a>
    
---
<br>
<h4 align="center"> Video available on YouTube.

<p align="center" >
<a href="https://youtu.be/XoSLzEDFRyE?si=PwjgHVsQ_5l6QVAP"><img src="https://img.shields.io/badge/DM%20Me-E4405F?style=for-the-badge&logo=youtube&logoColor=white" width="140px" height="40">
</a>
</p>

<h4 align="center"> Feel free to DM me if you face any error,bug or need help. You can also suggest me new features to add.

<p align="center" >
<a href="https://www.instagram.com/phoenix.site?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="><img src="https://img.shields.io/badge/DM%20Me-E4405F?style=for-the-badge&logo=instagram&logoColor=white" width="140px" height="40">
</a>
</p>
    
---
<br>

## Functions 

- General Interaction:
Responds to various general inquiries and commands.

- Open Applications:
YouTube,
Google Chrome,
Terminal (Command Prompt),
Visual Studio Code,
Instagram,
Notepad,
WhatsApp Web,
GitHub Profile,

- Close Applications:
Visual Studio Code,
Notepad,
Microsoft Edge,
Chrome Browser,
YouTube,

- Weather Updates:
Fetches and provides current weather information for specified locations using OpenWeatherMap API.

- YouTube Search:
Searches YouTube and plays the first video based on the given query.

- Text Writing:
Writes provided text in Notepad.

- Speed Test:
Measures and reports the current internet speed, including download speed, upload speed, and ping.

- Place Locator:
Opens Google Maps to search for specified places near the user's location.

- Website Opener:
Opens specified websites in the browser.

- Time and Date:
Provides the current time and date based on the system clock.

- Character Information:
Responds to questions about its developer and character name.

- Command Control:
Enables and disables command-taking based on user requests.

- Special Character AI Interaction:
Generates intelligent responses using Character AI for more complex or unique queries.

- Google GenAI Integration:
Generates content or responses using Google GenAI for specific requests, such as writing text in Notepad.

## API'S Used

 - [Gemini API](https://ai.google.dev/?gad_source=1&gclid=Cj0KCQjw6auyBhDzARIsALIo6v9ti61NHvqFunUKsMwzEVwtjtdP0h69vNzHCWMRG4zVbRy6mCNmcJMaAuQCEALw_wcB)
 - [TTS from Openai API](https://platform.openai.com/docs/guides/text-to-speech)
 - [CharacterAi API](https://beta.character.ai/chats)
 - [YT data API](https://developers.google.com/youtube/v3)
 - [Weather API](https://api.openweathermap.org/data/2.5/weather)

## Installation

1. Install the required dependencies (Might be lacking some)

```
pip install -r requirements.txt
```

2. Add your API keys and edit names in config.py 

```
OPENAI_API="YOUR OPENAI API KEY"
GEMINI_API="YOUR GEMINI API KEY"
YOUTUBE_API="YOUR YOUTUBE DATA API KEY"
WEATHER_API="YOUR WEATHER API KEY"
CHARACTER_AI_API="YOUR CHARACTERAI API KEY"
CHARACTER_ID="YOUR CHARACTERAI API KEY"
CHARACTER_NAME="AVA"
YOUR_NAME="Ronen"
```

3. Run gui.py

```
python3 gui.py
```
