from fastapi import APIRouter, HTTPException, UploadFile, File, Request
import speech_recognition as sr
import speech_recognition as sp
import datetime
import pyttsx3
import webbrowser
import openai
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import urllib.parse
import time
import googleapiclient.discovery



router = APIRouter(tags=["voice-assistant"])
openai.api_key = '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'

engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1) 

recognizer = sp.Recognizer()


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and return it as text."""
    with sp.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sp.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return ""
        except sp.RequestError:
            print("Sorry, there is an issue with the service.")
            speak("Sorry, there is an issue with the service.")
            return ""

def tell_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def open_website(url):
    """Open a website."""
    webbrowser.open(url)
    speak("on my way ")

templates = Jinja2Templates(directory="backend/templates")

@router.get("/listenwithout", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    """Render the registration HTML form."""
    return templates.TemplateResponse("listenwithout.html", {"request": request})

@router.post("/listenwithout")
async def voice_assistant():
    command = listen()  
    if not command:
        return {"message": "Sorry, I couldn't understand your command."}

    if "time" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        response = f"The time is {current_time}."
    elif "open" in command and "youtube" in command:
        if "song" in command:  
            song_name = command.replace("open youtube song", "").strip()
            if song_name:
                song_query = urllib.parse.quote_plus(song_name)
                url = f"https://www.youtube.com/results?search_query={song_query}"
                open_website(url)
                response = f"Searching for '{song_name}' on YouTube."
                
                video_url = f"https://www.youtube.com/watch?v={get_video_id_from_search(song_query)}"
                open_website(video_url)  
                response += f" Now playing '{song_name}'."
            else:
                response = "Please specify the song you want to search for on YouTube."
        else:
            url = "https://www.youtube.com" 
            open_website(url)
            response = "Opened YouTube as requested."
    elif "open" in command and "wikipedia" in command:
        url = "https://www.wikipedia.org" 
        open_website(url)
        response = "Opened Wikipedia as requested."
    elif "open" in command and "google" in command:
        url = "https://www.google.com" 
        open_website(url)
        response = "Opened Google as requested."
   
    elif "weather" in command:
        location = command.replace("weather", "").strip()
        if location:
            weather_info = get_weather(location)
            speak(weather_info)
            response = weather_info
        else:
            response = "Please specify a location for the weather."
    elif "add task" in command:
        task = command.replace("add task", "").strip()
        if task:
            response = add_task(task)
            speak(response)
        else:
            response = "Please specify the task you want to add."
    elif "show tasks" in command:
        response = get_tasks()
        speak(response)
    elif "search" in command and "google" in command:
        search_query = command.replace("search google", "").strip()
        if search_query:
            response = search_google(search_query)
        else:
            response = "Please specify what you want to search for on Google."

    else:
        response = "Sorry, I don't recognize that command."
        speak(response)

    # Return the result as JSON
    return {"message": response}

def get_video_id_from_search(query):
    api_key = "AIzaSyDDGeh-zPVCjRldAZkapDjUnRCxASrEfAk"
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        q=query,
        part="id",
        maxResults=1,
        type="video"
    )
    response = request.execute()
    video_id = response["items"][0]["id"]["videoId"]
    return video_id

def get_weather(location):
    api_key = "bf6497e4dbec1bc85e1511a420b69048"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
    response = requests.get(url).json()
    
    if response.get("cod") == 200:
        main = response["main"]
        weather = response["weather"][0]["description"]
        temp = main["temp"]
        return f"The temperature in {location} is {temp:.2f}°C with {weather}."
    else:
        return f"Error: {response.get('message', 'Could not retrieve weather data.')}"


tasks = []

def add_task(task):
    tasks.append(task)
    return f"Task '{task}' added to your to-do list."

def get_tasks():
    if tasks:
        return "\n".join(tasks)
    else:
        return "You have no tasks in your to-do list."

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    open_website(url)
    return f"Searching for '{query}' on Google."


