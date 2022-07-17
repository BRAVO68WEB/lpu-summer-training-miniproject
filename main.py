import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests
from newsapi import NewsApiClient
from bs4 import BeautifulSoup as bs

engine = pyttsx3.init("espeak")
voices = engine.getProperty('voices')
voices = engine.setProperty('gender', 'female')
engine.setProperty('voice', 'voices[1].id')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-24)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Hello,Good Morning it's {strTime}")
        print("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Hello,Good Afternoon it's {strTime}")
        print("Hello,Good Afternoon")
    else:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Hello,Good Evening it's {strTime}")
        print("Hello,Good Evening")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"User Voice Imput :{statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


print("Loading your AI personal assistant")
speak("Vector Booting Up !")
wishme()

if __name__ == '__main__':

    while True:
        speak("Listening")
        statement = takecommand().lower()

        if statement == 0:
            continue

        elif "stop" in statement or "see you later" in statement:
            speak('Vector is shutting down')
            print('Vector is shutting down,Good bye')
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening youtube")
            time.sleep(5)

        elif 'open browser' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening it right up next")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("GMail opens now")
            time.sleep(5)

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'can i ask you something' in statement:
            speak('Ask me anything !')
            question = takecommand()
            app_id = "GKJKY3-94XLLE9P4V"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "check weather" in statement:
            api_key = "3aec247a6a4ee14428a204ce083fab66"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name")
            city_name = takecommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

        elif "check headlines" in statement:
            newsapi = NewsApiClient(api_key='5fc464a7136147a69ce2b3c54761481d')
            source = "the-times-of-india"
            top_headlines = newsapi.get_top_headlines(sources=source)
            articles = top_headlines["articles"]
            for article in articles:
                print(article["title"])
                print(article["description"])
                print(article["url"])
                print("\n")
                speak(article["title"])
                time.sleep(1)

        elif "tell me some quotes" in statement:
            response = requests.get(
                "https://quote-garden.herokuapp.com/api/v3/quotes/random")
            if response.status_code == 200:
                json_data = response.json()
                data = json_data['data']
                speak(data[0]['quoteText'])
            else:
                print("Error while getting quote")

        elif "log off" in statement or "sign out" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

time.sleep(3)
