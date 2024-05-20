from tkinter import *
from threading import Thread
#import pyttsx3
import cv2
from PIL import Image, ImageTk
import time
import pygame
import requests
import json
import main 
from pydub import AudioSegment
from io import BytesIO
import config
import asyncio
import numpy as np  # Added import for numpy

# Define a global variable to track if the code should stop
should_stop = False
# Define global variables
#recognizing_label = None

def start_listening():
    global listening_label
    listening_label.config(text="")  # Update label text to show listening status
    main.take_command()  # Call the corresponding function from main.py
    listening_label.config(text="")  # Update label text to show not listening status

async def listen():
    global should_stop
    while True:  # Continuous listening loop
        try:
            query = main.take_command()  # Get voice input using main.py function
            if query:
                response = await main.reply(query)  # Get response using main.py function asynchronously
                update_reply(response)  # Update label with the reply text
                generate_speech(response)  # Generate speech from the response text

                if query.lower() == "shutdown":
                    should_stop = True
                    break  # Stop the loop if the user says "shutdown"
                elif query.lower() == "go full screen":
                    root.attributes("-fullscreen", True)  # Switch to full screen
                    set_fullscreen_video()  # Adjust video size and position for fullscreen
                elif query.lower() == "go small screen":
                    root.attributes("-fullscreen", False)  # Switch to small screen
                    set_small_screen_size()  # Adjust UI components for small screen

        except Exception as e:
            print("Error:", e)
        finally:
            await asyncio.sleep(0.1)  # Use asyncio.sleep for asynchronous sleeping within the loop
    if should_stop:
        root.quit()  # Quit the GUI application if should_stop is True

def listen_thread():
    asyncio.run(listen())

# Start the listening thread
listening_thread = Thread(target=listen_thread)
listening_thread.start()

def generate_speech(text):
    # API endpoint and your API key
    API_ENDPOINT = "https://api.openai.com/v1/audio/speech"
    API_KEY = config.OPENAI_API

    # Define headers with API key
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Create data payload with input text, model, and voice
    data = {
        "model": "tts-1",  # You can use 'tts-1' or 'tts-1-hd' as the model
        "input": text,
        "voice": "nova",  # Choose one of the supported voices: alloy, echo, fable, onyx, nova, shimmer
        "response_format": "mp3",  # Optional: Specify the audio format (mp3, opus, aac, flac, wav, pcm)
    }

    # Send POST request to the API endpoint
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Extract audio content from the response
        audio_content = response.content

        # Convert audio content to an audio stream
        audio_stream = BytesIO(audio_content)
        audio_segment = AudioSegment.from_file(audio_stream, format="mp3")

        # Play the audio stream using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(audio_segment.export(format="mp3"))
        pygame.mixer.music.play()

        print("Replied successfully.")
    else:
        print(f"Error: Failed to generate audio ({response.status_code}).")
        print(response.text)  # Print response content for debugging

def update_reply(text):
    subtitle_label.config(text=text)  # Update subtitle label with the response

import numpy as np  # Add this import at the top of your script

def resize_and_center_frame(frame, target_width, target_height):
    """Resize the frame to fill the target size while maintaining the aspect ratio and center it."""
    height, width, _ = frame.shape
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        # Video is wider than the target aspect ratio
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Video is taller than the target aspect ratio
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Calculate the center crop region
    x_start = (new_width - target_width) // 2
    y_start = (new_height - target_height) // 2
    cropped_frame = resized_frame[y_start:y_start + target_height, x_start:x_start + target_width]

    return cropped_frame

def play_video():
    """Function to play the video in the background."""
    try:
        global video_label, video_reply_label
        video_path = 'C:/Ava/assets/Ava.mp4'  # Update with your video file path
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Error opening video: {video_path}")

        while True:  # Loop to continuously play the video
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = resize_and_center_frame(frame, root.winfo_width(), root.winfo_height())  # Resize frame to fit the window
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                video_label.config(image=img)
                video_label.image = img

                root.update()
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Seek back to the beginning of the video
                continue  # Continue playing the video in a loop

        cap.release()
    except Exception as e:
        print("Error playing video:", str(e))
        
def set_small_screen_size():
    """Function to set the UI components for small screen."""
    global listening_label, speaking_label, subtitle_label
    # Set window size to 9:16 aspect ratio
    small_height = 900
    small_width = int(small_height * 9 / 16)
    root.geometry(f"{small_width}x{small_height}")

    # Calculate scaling factors based on screen resolution
    label_scale = int(small_width / 110)  # Adjust label size based on screen width

    # Configure label font size based on scaling factor
    listening_label.config(font=('Arial', label_scale))
    speaking_label.config(font=('Arial', label_scale))

    # Create subtitle label
    subtitle_label = Label(root, text="", font=('Arial', 24, 'bold'), bg='black', fg='white')
    subtitle_label.pack(fill=X, side=BOTTOM)

def set_fullscreen_video():
    """Function to adjust video size and position for fullscreen."""
    global video_label, video_reply_label, subtitle_label
    video_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place video label in fullscreen
    subtitle_label.lift()  # Bring subtitle label to front

"""def play_intro_audio():
    #Function to play the intro audio
    try:
        pygame.mixer.init()
        intro_audio = pygame.mixer.Sound('C:/Ava/assets/Aiden_intro.mp3')  # Update with your audio file path
        intro_audio.play()
    except Exception as e:
        print("Error playing intro audio:", str(e))"""

def play_intro_audio():
    """Function to generate and play the intro audio."""
    intro_text = "Hello there! I am AVA, Your virtual assistant based on anime theme, How can I help you today?"
    generate_speech(intro_text)

def change_video_theme(video_path):
    global video_thread
    try:
        if video_thread.is_alive():  # Check if the previous video thread is running
            video_thread.stop()  # Stop the previous video thread
    except AttributeError:
        pass  # Ignore if video_thread is not defined yet

    # Start a new video thread with the specified video path
    video_thread = Thread(target=play_specific_video, args=(video_path,))
    video_thread.start()      

#def set_video_theme(theme_name):
#    if theme_name.lower() == "green":
#        change_video_theme('C:/Users/Owner/Documents/My codes/Aiden Main/assets/Aiden_green.mp4')
#    elif theme_name.lower() == "red":
#       change_video_theme('C:/Users/Owner/Documents/My codes/Aiden Main/assets/Aiden_red.mp4')
#    elif theme_name.lower() == "blue":
#        change_video_theme('C:/Users/Owner/Documents/My codes/Aiden Main/assets/Aiden_blue.mp4')
    # Add more theme options as needed

def play_specific_video(video_path):
    """Function to play a specific video."""
    try:
        global video_label
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Error opening video: {video_path}")

        while True:  # Loop to continuously play the video
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = resize_and_center_frame(frame, root.winfo_width(), root.winfo_height())  # Resize frame to fit the window
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                video_label.config(image=img)
                video_label.image = img

                root.update()
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Seek back to the beginning of the video
                continue  # Continue playing the video in a loop

        cap.release()
    except Exception as e:
        print("Error playing video:", str(e))

root = Tk()
root.title(config.CHARACTER_NAME)
root.resizable(False, False)

# Create a label for displaying the video
video_label = Label(root)
video_label.pack(fill=BOTH, expand=YES)

# Label for video reply display (to replace the conversation text)
video_reply_label = Label(root, text="", font=('Arial', 12, 'bold'), bg='black', fg='white')
video_reply_label.pack(fill=X, side=BOTTOM)

# Initialize pyttsx3 engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
# engine.setProperty('rate', 180)

# Define your labels
listening_label = Label(root, text="", font=('Arial', 12, 'bold'))
listening_label.pack()

speaking_label = Label(root, text="Listening...", font=('Arial', 12, 'bold'))
speaking_label.pack()

# Set small screen size initially
set_small_screen_size()

# Start the listening thread
listening_thread = Thread(target=listen)
listening_thread.start()

# Start the video playback
video_thread = Thread(target=play_video)
video_thread.start()

# Play the intro audio after a short delay (to allow GUI initialization)
root.after(1000, play_intro_audio)

# Call the set_fullscreen_video function to adjust video size and position for fullscreen
set_fullscreen_video()

root.mainloop()