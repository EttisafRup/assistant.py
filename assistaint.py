import os
from bs4 import BeautifulSoup
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import webbrowser
import urllib.request
import re
import wikipedia
import random


# Clearing the Terminal every time it runs
os.system("clear")

engine = pyttsx3.init("sapi5")
engine_voice = engine.getProperty("voices")
engine.setProperty("voice", engine_voice[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    pass


def wishGood():
    time_hour = datetime.datetime.now()
    day_or_night = "AM" if time_hour.hour <= 12 else "PM"
    if time_hour.hour >= 0 and time_hour.hour <= 12:
        print("Good Morning Sir")
        speak("Good Morning Sir")
    elif time_hour.hour > 12 and time_hour.hour <= 18:
        print("Good Afternoon Sir")
        speak("Good Afternoon Sir")
    elif time_hour.hour > 18 and time_hour.hour <= 23:
        print("Good Evening Sir")
        speak("Good Evening Sir")
    else:
        speak("I cant figure but Welcome back, sir!")

    speak(f"It's {time_hour.hour}, {time_hour.minute} {day_or_night}")
    print("Lisa here! please let me know if you need any kind of help in your activities!")
    speak("Lisa here! please let me know if you need any kind of help in your activities!")


def takeCommand():
    """It's a function which allows us to input from the user through mic"""

    micRecognizer = sr.Recognizer()

    with sr.Microphone() as micro:
        print("Lisa is Listening...")
        micRecognizer.pause_threshold = 1
        micRecognizer.adjust_for_ambient_noise(micro)
        audio = micRecognizer.listen(micro)

    try:
        print("Lisa is figuring it out...")
        query = micRecognizer.recognize_google(audio, language="en-In")
        return query
    except:
        return "nothing"


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    wishGood()
    while 1:
        query = takeCommand().lower()
        print(query)
        if "youtube" in query:

            givenCommand = query[0:query.index(
                "youtube")] if "youtube" in query else query
            searchText = "+".join(givenCommand.split(" "))

            get_html_code = urllib.request.urlopen(
                f"https://www.youtube.com/results?search_query={searchText}").read().decode()
            video_watchLinks = re.findall(r"watch\?v=(\S{11})", get_html_code)

            pyautogui.hotkey('space')
            webbrowser.open(
                f"https://www.youtube.com/watch?v={video_watchLinks[0]}")
            speak("Playing Video from Youtube, Enjoy")

        elif "facebook" in query:

            webbrowser.open("https://www.facebook.com/")
            speak("Facebook is opened!")

        elif "messenger" in query:
            webbrowser.open(
                "https://www.messenger.com/")
            speak("Messenger opened!")

        elif "google" in query:
            webbrowser.open(
                "https://www.google.com/")
            speak("Google opened!")

        elif "pause" in query or "play" in query:
            pyautogui.hotkey("space")

        elif "close chrome" in query or "the chrome" in query:
            os.system("taskkill /im chrome.exe /f")
            speak("Chrome was closed!")

        elif "close" in query or "the tab" in query:
            pyautogui.hotkey("ctrl", "w")
            speak("Tab was closed!")

        elif "temperature" in query:
            try:
                res = requests.get(
                    f'https://www.timeanddate.com/weather/bangladesh/dhaka', headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                temp = soup.select('.h2')[0].getText().strip()
                print(f"The current temperature is {temp}elcius")
                speak(f"The current temperature is {temp}elcius")
            except:
                speak("Something went wrong on the cloud, try something else..!")

        elif "screenshot" in query:
            if not os.path.exists(os.path.join(os.getcwd(), "screenshot")):
                os.mkdir(os.path.join(os.getcwd(), "screenshot"))

            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(os.path.join(
                f"screenshot\screenshot{random.randint(0,100)}.png"))
            speak("Screenshot saved on the screenshot direcotory!.")

        elif "type" in query:
            speak("Typing on the target in 3, 2, 1..")
            pyautogui.write(query[query.index("type")+5:] + " ")

        elif "enter" in query:
            pyautogui.hotkey("enter")
            speak("Enter was pressed!")

        elif "undo" in query:
            pyautogui.hotkey("ctrl", "z")
            speak("Undo done!")

        elif "remove" in query:
            pyautogui.hotkey("ctrl", "backspace")
            speak("One word removed successfully!")

        elif any(s in query for s in ("search", "wikipedia", "who", "what", "where", "how", "when", "whom")):
            try:
                query = query.replace("search", "")
                query = query.replace("wikipedia", "")
                query = query.replace("on", "")
                query = query.replace("from", "")

                result = wikipedia.summary(query, sentences=2)
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak(result)
            except:
                speak("Something went wrong on the cloud, try something else..!")

        elif "exit" in query or "bye" in query or "off" in query or "quit" in query:
            speak("Lisa is signing off, Have a good day sir! Bye!")
            exit()

        elif any(s in query for s in ("okay", "thank", "my love")):
            speak("Sir it's my pleasure! Call me anytime")

        elif any(s in query for s in ("lisa", "hello", "hi", "laser", "blazer")):
            speak("Lisa is listening sir!!")

        else:
            speak(
                f"I'm not sure but I heard {query}, I did not understand what to do. Please say that again!")
