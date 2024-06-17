import speech_recognition as sr
import webbrowser
import google.generativeai as genai
import requests
from datetime import datetime
import os
import pygame
from bs4 import BeautifulSoup
import time 
import config
import pyautogui
from characterai import aiocai
import asyncio
import speedtest
import re

genai.configure(api_key=config.GEMINI_API)

youtube_api_key = config.YOUTUBE_API

api_key = config.WEATHER_API
base_url = 'https://api.openweathermap.org/data/2.5/weather'

pygame.mixer.init()

take_command_flag = True

character_id = config.CHARACTER_ID
character_ai_client = aiocai.Client(config.CHARACTER_AI_API) 

async def get_character_ai_response(question):
    me = await character_ai_client.get_me()
    async with await character_ai_client.connect() as chat:
        new, answer = await chat.new_chat(character_id, me.id)
        message = await chat.send_message(character_id, new.chat_id, question)
        return message.text.strip()

def delayed_start():
    time.sleep(8)  
    while True:
        query = take_command()
        if query == "":
            continue

        ans = asyncio.run(reply(query))
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        if 'open google' in query:
            webbrowser.open("www.google.com")
        if 'shutdown' in query:
            break

def speak(text):
    """Function to speak the provided text."""

def take_command():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.energy_threshold = 4000 
        audio = r.listen(source, timeout=None) 
        
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print("You Said:", query)
        return query.lower()
    except Exception as e:
        print("Say That Again....")
        return ""

if __name__ == '__main__':
    while True:
        query = take_command()
        if query:
            print("Query Detected:", query)
            break

def get_weather(location):
    try:
        url = f"{base_url}?q={location}&units=metric&appid={api_key}&lang=en"
        response = requests.get(url)
        weather_data = response.json()
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        weather_report = f"The weather in {location} is {weather_description}. " \
                         f"The temperature is {temperature}°C, " \
                         f"humidity is {humidity}%, " \
                         f"and wind speed is {wind_speed} m/s."
        return weather_report
    except Exception as e:
        print("Error fetching weather data:", str(e))
        return "Failed to fetch weather data."

def search_youtube(query):
    try:
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={youtube_api_key}"
        response = requests.get(search_url)
        videos = response.json()['items']
        if videos:
            video_id = videos[0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return None
    except Exception as e:
        print("Error searching YouTube:", str(e))
        return None

def open_notepad_and_write(reply_text):
    # Open Notepad using the 'os' module
    os.system("start notepad")

    time.sleep(2)

    lines = reply_text.split('\n')

    for line in lines:
        pyautogui.typewrite(line)
        pyautogui.press('enter') 

async def reply(question):
    global take_command_flag

    if 'in notepad' in question:
        question = question.replace('in notepad', '').strip()
        
        response = genai.GenerativeModel('gemini-pro').generate_content(
            f"question: {question}\nAct and reply like you are {config.CHARACTER_NAME} an anime inspired virtual assistant:")
        
        reply_text = response.text.strip()
        
        open_notepad_and_write(reply_text)

        return "I wrote down your text in Notepad."

    if 'don\'t take command' in question:
        take_command_flag = False
        return "Command-taking disabled."
    elif 'take command' in question:
        take_command_flag = True
        return "Command-taking enabled."

    if not take_command_flag:
        print("Listening without replying...")
        return

    if 'ronen' in question and 'developer' in question:
        return "I was developed by Ronen in May 2024."
    elif 'Who is Ronen' in question:
        return "Ronen is my developer."
    elif 'Who is your developer' in question:
        return "I was developed by Ronen in May 2024."
    elif 'Who is your creator' in question:
        return "I was created by Ronen in May 2024."
    elif 'what is my name' in question:
        return f"Your name is {config.YOUR_NAME}."
    elif 'what is your name' in question:
        return f"I am Autonomous Virtual Assistant, in short {config.CHARACTER_NAME}, created by Ronen."
    elif 'your name' in question:
        return f"I am Autonomous Virtual Assistant, in short {config.CHARACTER_NAME}, created by Ronen."
    elif 'who are you' in question:
        return f"I am Autonomous Virtual Assistant, in short {config.CHARACTER_NAME}, created by Ronen."
    elif 'who am i' in question:
        return f"You are {config.YOUR_NAME}."
    elif 'change theme to blue' in question:
        return "Changing theme to Blue."
    elif 'change theme to green' in question:
        return "Changing theme to Green."
    elif 'change theme to red' in question:
        return "Changing theme to Red."
    elif 'what is the time now' in question:
        now = datetime.now().strftime("%H:%M:%S")
        return f"The current time in India is {now}."
    elif 'what is the date today' in question:
        date_today = datetime.now().strftime("%m/%d/%Y")
        return f"Today's date in India is {date_today}."
    elif 'weather' in question:
        location = question.split('weather')[1].strip() 
        return get_weather(location)
    elif 'shutdown' in question:
        return "System shutting down. Goodbye Ronen, Have a nice day."
    elif 'go full screen' in question:
        return "Going Full screen."
    elif 'go small screen' in question:
        return "Going Small screen."
    # Open Youtube
    elif 'open youtube' in question:
        youtube_path = 'C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/YouTube'
        os.startfile(youtube_path)
        return "Opening Youtube."
    # Open Google
    elif 'open google' in question:
        chrome_path = 'C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Google Chrome'
        os.startfile(chrome_path)
        return "Opening Google."
    # Open Terminal
    elif 'open terminal' in question:
        terminal_path = 'C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/System Tools/Command Prompt'
        os.startfile(terminal_path)
        return "Opening Terminal."
    # Open VScode
    elif 'open vs code' in question:
        vscode_path = 'C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code'
        os.startfile(vscode_path)
        return "Opening VScode."
    # Open Instagram
    elif 'open instagram' in question:
        instagram_path = 'C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Instagram'
        os.startfile(instagram_path)
        return "Opening Instagram."
    # Open Notepad
    elif 'open notepad' in question:
        notepad_path = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Accessories/Notepad'
        os.startfile(notepad_path)
        return "Opening Notepad."
    # Open Whatsapp
    elif 'open whatsapp' in question:
        webbrowser.open('https://web.whatsapp.com/')
        return "Opening WhatsApp."
    # Open Github
    elif 'open github' in question:
        webbrowser.open('https://github.com/Ronen6999')
        return "Opening Github."
    # Close VScode
    elif 'close vs code' in question:
        os.system("taskkill /f /im Code.exe /t")
        return "Closing VScode."
    # Run Speed Test
    elif 'run speed test' in question:
        return speed_test()
     # Get places near me
    elif 'locate' in question:
        place_query = question.replace('locate', '').strip()
        return get_places_near_me(query=place_query)
    # Open website
    elif 'open website' in question:
        website_query = question.replace('open website', '').strip()
        website_opener(query=website_query)
        return f"Opening {website_query}."
    elif 'close chrome' in question and 'close google' in question:
        os.system("taskkill /f /im chrome.exe /t")
        return "Closing Chrome."
    # Close Notepad
    elif 'close notepad' in question:
        os.system("taskkill /f /im notepad.exe /t")
        return "Closing Notepad."
    # Close Microsoft Edge
    elif 'close microsoft edge' in question:
        os.system("taskkill /f /im msedge.exe /t")
        return "Closing Microsoft Edge."
    # Close Youtube
    elif 'close youtube' in question:
        os.system("taskkill /f /im msedge.exe /t")
        return "Closing Youtube."
    # Search YouTube and play the first video automatically
    elif 'play' in question:
        search_query = question.split('play')[1].strip()
        video_url = search_youtube(search_query)
        if video_url:
            webbrowser.open(video_url)
            return f"Playing '{search_query}' on YouTube."
        else:
            return f"Unable to find results for '{search_query}' on YouTube."
    else:
        response = await get_character_ai_response(question)
        return response
    
    # Speed test functions
try:
    st = speedtest.Speedtest()
except:
    print("Please check your internet connection.")
    pass

def download_speed():
    down = round(st.download() / 10 ** 6, 2)
    return down

def upload_speed():
    up = round(st.upload() / 10 ** 6, 2)
    return up

def ping():
    servernames = []
    st.get_servers(servernames)
    results = st.results.ping
    return results

def speed_test(*args, **kwargs):
    try:
        print("Checking internet speed. Please wait...")
        return "Download Speed: " + str(download_speed()) + "MB/s" + "\n Upload Speed: " + str(
            upload_speed()) + " MB/s" + "\n Ping: " + str(ping()) + " ms"
    except Exception as e:
        print(e)
        return "Error in internet speed test"
    
    # Get places near me function
def get_places_near_me(*args, **kwargs):
    inp_command = kwargs.get("query")
    map_base_url = f"https://www.google.com/maps/search/{inp_command}"
    webbrowser.open(map_base_url)
    return f"Here are some {inp_command} near you"

def website_opener(*args, **kwargs):
    input_text = kwargs.get("query")
    domain = input_text.lower().split(" ")[-1]
    extension = re.search(r"[.]", domain)
    if not extension:
        if not domain.endswith(".com"):
            domain = domain + ".com"
    try:
        url = 'https://www.' + domain
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    asyncio.run(delayed_start())

