import json
import requests    
import datetime    
import random    
import json    
import subprocess    

import pyaudio

import sounddevice as sd
from scipy.io.wavfile import write
import wave
import json
import numpy as np
import soundfile

import whisper

#from gtts import gTTS    
#from gtts import gTTS    
#from io import BytesIO    
#from pydub import AudioSegment    
#from pydub.playback import play    

def int32_to_int16(audio_file):
    data, samplerate = soundfile.read(audio_file)
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')

file="/home/ubie/smartMirrorV2/voice-assistant/output.wav"


def record():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording
    channels = 2 # mono recording
    
    print("Recording audio...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels, dtype=np.float32)
    sd.wait()  # Wait until recording is finished
    
    print("Saving audio to WAV file...")
    write('output.wav', fs, myrecording)


model = whisper.load_model("tiny")

def stt(audio_file):
    result = model.transcribe(audio_file, fp16=False)
    print(result["text"])
    return(result["text"])    
#    subprocess.run(["/home/ubie/smartMirrorV2/voice-assistant/stt.sh",string],shell=False)


def get_audio():
    record()
    return stt(file)
'''
def speech(arg):
    mp3_fp = BytesIO()
    tts = gTTS(arg, lang='en')
    tts.write_to_fp(mp3_fp)

    # Rewind the BytesIO object
    mp3_fp.seek(0)

    # Load MP3 data into AudioSegment
    audio_segment = AudioSegment.from_mp3(mp3_fp)

    # Play the audio
    play(audio_segment)
'''
def speak(string): 
    subprocess.run(["/home/ubie/smartMirrorV2/voice-assistant/tts.sh",string],shell=False)

'''
def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print(e)
            return ""
'''
def load_events():
    try:
        with open("events.json", "r") as file:
            data = file.read()
            if data:
                return json.loads(data)
            else:
                return {}  # Return an empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist
    except json.decoder.JSONDecodeError:
        return {}  # Return an empty dictionary if the file contains invalid JSON data

def save_events(events_dict):
    with open("events.json", "w") as file:
        json.dump(events_dict, file)

def get_event_title():
    while True:
        speak("Please say the title of the event.")
        #speech("Please say the title of the event")
        title = get_audio()
        if title:
            return title
        else:
            #speech( "Sorry, I didn't catch that. Please try again.")
            speak("Sorry, I didn't catch that. Please try again.")

def get_event_date():
    while True:
        speak("Please say the date of the event.")
        #speech("Please say the date of the event")
        date = get_audio()
        if date:
            return date
        else:
            #speech("Sorry, I didn't catch that. Please try again.")
            speak("Sorry, I didn't catch that. Please try again.")

def store_event(event_title, event_date, events_dict):
    events_dict[event_title] = event_date
    save_events(events_dict)  # Save events to file after storing
    return "Event stored successfully!"

def get_event(event_title, events_dict):
    if event_title in events_dict:
        return f"The event '{event_title}' is scheduled on {events_dict[event_title]}."
    else:
        return f"Sorry, there is no event titled '{event_title}' stored."

def get_weather():
    api_key = "3ed3625376c65ae31fb416c1f5c76e6f"
    city = "Delhi"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather is {weather} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, unable to fetch weather information."


def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def get_news():
    api_key = "f4ced57051b64ddabd60e674941828f8"
    url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        articles = data['articles'][:5]
        news = "Here are the top headlines: "
        for article in articles:
            news += article['title'] + ". "
        return news
    else:
        return "Sorry, unable to fetch news."

def suggest_movie():
    try:
        response = requests.get("https://api.themoviedb.org/3/discover/movie", params={
            "api_key": "905bf24ae08fc57b2cbe70eecd2a92cf",
            "sort_by": "popularity.desc"
        })
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            movie = random.choice(data['results'])['title']
            return f"I suggest you watch {movie}!"
        else:
            return "Sorry, I couldn't find any movie recommendations at the moment."
    except Exception as e:
        print(e)
        return "Sorry, I encountered an error while fetching movie recommendations."

def self_description():
    return "I am a smart E bulletin board made by the department of Electronics and Communications BPIT"

def handle_query(query, events_dict):
    if "weather" in query:
        return get_weather()
    elif "time" in query:
        return f"The current time is {get_time()}."
    elif "news" in query:
        return get_news()
    elif "movie" in query:
        return suggest_movie()
    elif "purpose" in query:
        return self_description()
    elif "store event" in query:
        speak("Sure, let's store the event.")
        #speech("Sure, let's store the event.")
        event_title = get_event_title()
        event_date = get_event_date()
        return store_event(event_title, event_date, events_dict)
    elif "get event." in query:
        speak("Sure, let's retrieve the event.")
        #speech("Sure, let's retrieve the event")
        event_title = get_event_title()
        return get_event(event_title, events_dict)
    elif "schedule" in query:
        return read_schedule(query)
    else:
        return "Sorry, I didn't understand that."
'''
def listen_for_wake_word(wake_word="hey assistant"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio, language='en-in')
                if wake_word in query.lower():
                    print("Wake word detected!")
                    return True
            except Exception as e:
                print(e)
                continue
'''

file="/home/ubie/smartMirrorV2/voice-assistant/output.wav"
def listen_for_wake_word(wake_word="hey assistant"):
    while True:
        record()
        text = stt(file)                                                   
        print(text.lower())
        if wake_word in text.lower():
            return True
        else:
            continue


def read_schedule(query):
    current_day = datetime.datetime.now().strftime("%A")
    
    if "today" in query:
        if current_day in schedule["week"]:
            day_schedule = schedule["week"][current_day]
            schedule_text = f"The schedule for {current_day} is as follows:\n"
            for time_slot, info in day_schedule.items():
                if "break" not in info:
                    lecture = info.get('lecture', 'No lecture information available')
                    lecturer = info.get('lecturer', 'No lecturer information available')
                    schedule_text += f"At {time_slot}, {lecture} by {lecturer}\n"
            return schedule_text
        else:
            return "Sorry, I couldn't find the schedule for today."
    
    elif "schedule for" in query:
        for day, value in schedule["week"].items():
            if day.lower() in query:
                day_schedule = value
                schedule_text = f"The schedule for {day} is as follows:\n"
                for time_slot, info in day_schedule.items():
                    if "break" not in info:
                        lecture = info.get('lecture', 'No lecture information available')
                        lecturer = info.get('lecturer', 'No lecturer information available')
                        schedule_text += f"At {time_slot}, {lecture} by {lecturer}\n"
                return schedule_text
        return "Sorry, I couldn't find the schedule for that day."
    
    else:
        return "Sorry, I didn't understand. Please try again."
