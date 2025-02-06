from fastapi import APIRouter, HTTPException, UploadFile, File, Request
import speech_recognition as sr
import datetime
import pyttsx3
import webbrowser
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import urllib.parse
import time

router = APIRouter(tags=["voice-assistant"])

DEEPSEEK_API_KEY = 'sk-a03a675056884ee294a94c8f5075e242' 
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'  

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1)

recognizer = sr.Recognizer()

def speak(text):

    engine.say(text)
    engine.runAndWait()

def listen():

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there is an issue with the service.")
            speak("Sorry, there is an issue with the service.")
            return ""

def deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 200
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error from DeepSeek API: {e}"

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def open_website(url):
    webbrowser.open(url)
    speak("Opening the website.")

def open_youtube_video(video_query):
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(video_query)}"
    response = requests.get(search_url)
    if response.status_code == 200:
        webbrowser.open(search_url)
        speak(f"Searching for {video_query} on YouTube.")
    else:
        speak("Sorry, I couldn't search for the video on YouTube.")

templates = Jinja2Templates(directory="backend/templates")

@router.get("/voice", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    return templates.TemplateResponse("listen.html", {"request": request})

@router.post("/voice")
async def voice_assistant():
    command = listen()
    if not command:
        return {"message": "Sorry, I couldn't understand your command."}

    if "time" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        response = f"The time is {current_time}."

    elif "open" in command:
        if "youtube" in command:
            if "video" in command:
                video_query = command.replace("open youtube video", "").strip()
                open_youtube_video(video_query)
                response = f"Searching for {video_query} on YouTube."
            else:
                open_website("https://www.youtube.com")
                response = "Opened YouTube."
        elif "wikipedia" in command:
            open_website("https://www.wikipedia.org")
            response = "Opened Wikipedia."
        elif "google" in command:
            open_website("https://www.google.com")
            response = "Opened Google."
        else:
            response = "I don't know that website."

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

    elif "search google" in command:
        search_query = command.replace("search google", "").strip()
        if search_query:
            response = search_google(search_query)
        else:
            response = "Please specify what you want to search for on Google."

    elif "tell me a joke" in command:
        response = tell_joke()
        speak(response)

    elif "news" in command:
        response = get_news()
        speak(response)

    else:
        response = deepseek_response(command)
        speak(response)

    return {"message": response}

def get_weather(location):
    api_key = "05f4063dccc5011a2a6066b8617442fd"
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
    return "\n".join(tasks) if tasks else "You have no tasks in your to-do list."

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    open_website(url)
    return f"Searching for '{query}' on Google."

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
    ]
    return jokes[datetime.datetime.now().second % len(jokes)]

def get_news():
    news_api_key = "51008b130e6c4d8899691d6ff38df9c3" 
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        articles = response.get("articles", [])
        headlines = [article["title"] for article in articles[:5]]
        return "Here are the latest news headlines: " + ". ".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news at the moment."