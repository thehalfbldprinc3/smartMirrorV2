#import speech_recognition as sr
#import pyttsx3
import requests
import datetime
import random
import json
import subprocess
import sr

#from gtts import gTTS
#from gtts import gTTS
#from io import BytesIO
#from pydub import AudioSegment
#from pydub.playback import play


greetings = ["Hello! How can I assist you?",
             "Hi there! What can I do for you today?",
             "Hey! How may I help you?",
             "Greetings! What do you need assistance with?"]


def get_output(string): 
    subprocess.run(["/home/mirror/smartMirrorV2/voice-assistant/tts.sh",string],shell=False)
 

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
        #speak(engine, "Please say the title of the event.")
        #speech("Please say the title of the event")
        get_output("Please say the title of the event")
        title = sr.get_audio()
        if title:
            return title
        else:
            get_output( "Sorry, I didn't catch that. Please try again.")

def get_event_date():
    while True:
#        speak(engine, "Please say the date of the event.")
#        speech("Please say the date of the event")
        get_output("Please say the date of the event")
        date = sr.get_audio()
        if date:
            return date
        else:
            get_output("Sorry, I didn't catch that. Please try again.")

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
#        speak(engine, "Sure, let's store the event.")
#        speech("Sure, let's store the event.")
        get_output("Sure, let's store the event.")
        event_title = get_event_title()
        event_date = get_event_date()
        return store_event(event_title, event_date, events_dict)
    elif "get event" in query:
        #speak(engine, "Sure, let's retrieve the event.")
        #speech("Sure, let's retrieve the event")
        get_output("Sure let's retrive the event.")
        event_title = get_event_title()
        return get_event(event_title, events_dict)
    else:
        return "Sorry, I didn't understand that."

def main():
#    engine = initialize_engine()
    greeting = random.choice(greetings)
#    speak(engine, greeting)   
    get_output(greeting)    

    # Load events from file
    events_dict = load_events()
    
    while True:
        query = sr.get_audio()
        if query:
            if "exit" in query:
                # Save events to file before exiting
                save_events(events_dict)
                get_output("Goodbye!")
                return False

            if "restart" in query: 
                save_events(events_dict)
                get_output("Restarting E-bulletin board")
                return True

            response = handle_query(query, events_dict)
#            print(response)
            get_output(response)
#            speak(engine, response)
 
if __name__ == "__main__": 
    while True:
        if main():
            continue
        else:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            break
