from tkinter import *
from threading import Thread
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
import numpy as np  

should_stop = False

def start_listening():
    global listening_label
    listening_label.config(text="")  
    main.take_command() 
    listening_label.config(text="")  

async def listen():
    global should_stop
    while True:  
        try:
            query = main.take_command()  
            if query:
                response = await main.reply(query)  
                update_reply(response)  
                generate_speech(response)  

                if query.lower() == "shutdown":
                    should_stop = True
                    break 
                elif query.lower() == "go full screen":
                    root.attributes("-fullscreen", True)  
                    set_fullscreen_video()  
                elif query.lower() == "go small screen":
                    root.attributes("-fullscreen", False)  
                    set_small_screen_size() 
        except Exception as e:
            print("Error:", e)
        finally:
            await asyncio.sleep(0.1)
    if should_stop:
        root.quit()  

def listen_thread():
    asyncio.run(listen())

listening_thread = Thread(target=listen_thread)
listening_thread.start()

def generate_speech(text):
   
    API_ENDPOINT = "https://api.openai.com/v1/audio/speech"
    API_KEY = config.OPENAI_API

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "tts-1", 
        "input": text,
        "voice": "nova",  
        "response_format": "mp3", 
    }

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        audio_content = response.content

        audio_stream = BytesIO(audio_content)
        audio_segment = AudioSegment.from_file(audio_stream, format="mp3")

        pygame.mixer.init()
        pygame.mixer.music.load(audio_segment.export(format="mp3"))
        pygame.mixer.music.play()

        print("Replied successfully.")
    else:
        print(f"Error: Failed to generate audio ({response.status_code}).")
        print(response.text) 

def update_reply(text):
    subtitle_label.config(text=text) 

import numpy as np  

def resize_and_center_frame(frame, target_width, target_height):
    """Resize the frame to fill the target size while maintaining the aspect ratio and center it."""
    height, width, _ = frame.shape
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    resized_frame = cv2.resize(frame, (new_width, new_height))

    x_start = (new_width - target_width) // 2
    y_start = (new_height - target_height) // 2
    cropped_frame = resized_frame[y_start:y_start + target_height, x_start:x_start + target_width]

    return cropped_frame

def play_video():
    """Function to play the video in the background."""
    try:
        global video_label, video_reply_label
        video_path = 'C:/Ava/assets/Ava.mp4'
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Error opening video: {video_path}")

        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = resize_and_center_frame(frame, root.winfo_width(), root.winfo_height())  
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                video_label.config(image=img)
                video_label.image = img

                root.update()
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                continue 

        cap.release()
    except Exception as e:
        print("Error playing video:", str(e))
        
def set_small_screen_size():
    """Function to set the UI components for small screen."""
    global listening_label, speaking_label, subtitle_label
    small_height = 900
    small_width = int(small_height * 9 / 16)
    root.geometry(f"{small_width}x{small_height}")

    label_scale = int(small_width / 110)  

    listening_label.config(font=('Arial', label_scale))
    speaking_label.config(font=('Arial', label_scale))

    subtitle_label = Label(root, text="", font=('Arial', 24, 'bold'), bg='black', fg='white')
    subtitle_label.pack(fill=X, side=BOTTOM)

def set_fullscreen_video():
    """Function to adjust video size and position for fullscreen."""
    global video_label, video_reply_label, subtitle_label
    video_label.place(x=0, y=0, relwidth=1, relheight=1)  
    subtitle_label.lift() 


def play_intro_audio():
    intro_text = f"Hello there! I am {config.CHARACTER_NAME}, Your virtual assistant based on anime theme, How can I help you today?"
    generate_speech(intro_text)

def change_video_theme(video_path):
    global video_thread
    try:
        if video_thread.is_alive():  
            video_thread.stop() 
    except AttributeError:
        pass  

    video_thread = Thread(target=play_specific_video, args=(video_path,))
    video_thread.start()      

def play_specific_video(video_path):
    """Function to play a specific video."""
    try:
        global video_label
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Error opening video: {video_path}")

        while True:  
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = resize_and_center_frame(frame, root.winfo_width(), root.winfo_height())  
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                video_label.config(image=img)
                video_label.image = img

                root.update()
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
                continue  

        cap.release()
    except Exception as e:
        print("Error playing video:", str(e))

root = Tk()
root.title(config.CHARACTER_NAME)
root.resizable(False, False)

video_label = Label(root)
video_label.pack(fill=BOTH, expand=YES)

video_reply_label = Label(root, text="", font=('Arial', 12, 'bold'), bg='black', fg='white')
video_reply_label.pack(fill=X, side=BOTTOM)

listening_label = Label(root, text="", font=('Arial', 12, 'bold'))
listening_label.pack()

speaking_label = Label(root, text="Listening...", font=('Arial', 12, 'bold'))
speaking_label.pack()

set_small_screen_size()

listening_thread = Thread(target=listen)
listening_thread.start()

video_thread = Thread(target=play_video)
video_thread.start()

root.after(1000, play_intro_audio)

set_fullscreen_video()

root.mainloop()
