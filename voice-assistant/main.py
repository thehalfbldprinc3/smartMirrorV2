from functions import *
import json

greetings = ["Hello! How can I assist you?",
             "Hi there! What can I do for you today?",
             "Hey! How may I help you?",
             "Greetings! What do you need assistance with?"]

def main():
    events_dict = load_events()
    global schedule
    try:
        with open("schedule.json", "r") as file:
            schedule = json.load(file)
    except FileNotFoundError:
        return "Schedule file not found."
    except json.decoder.JSONDecodeError:
        return "Error decoding the schedule file."
    
    
    while True:
        if listen_for_wake_word():
            greeting = random.choice(greetings)
            speak(greeting)

            while True:
                query = get_audio()
                if query:
                    if "exit" in query:
                        # Save events to file before exiting
                        save_events(events_dict)
                        #speech("Goodbye!")
                        speak("Goodbye!")
                        return False

                    response = handle_query(query, events_dict)
                    #speech(response)
                    speak(response)


if __name__ == "__main__": 
    while True:
        if main():
            continue
        else:
            break

