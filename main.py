import pyttsx3
import speech_recognition as sr
import webbrowser as web
import pyautogui
import psutil
import screen_brightness_control as sb
import requests
import os
import pywhatkit
import pygame
from time import *
import datetime
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import wolframalpha


client = wolframalpha.Client("UQ94PG-K6X8UW4UEK") 

engine = pyttsx3.init()


def speak(text):
    engine = pyttsx3.init()
    if(text=="A string value is not answerable"):
        text="Sorry sir, I didn't get you. Please say that again"
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=5)  
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language='en-in')
            print(f"Your command is {query} ")
        except:
            return ""
    return query.lower()

def shut():
    speak("Your System will shutdown in 5 seconds")
    os.system("shutdown /s /t 5")
    music_path = "./count.mp3"
    playMusic(music_path)


def res():
    speak("Your System will restart in 5 seconds")
    os.system("shutdown /r /t 5")
    music_path = "./count.mp3"
    playMusic(music_path)

def googlemaps(place):
    geolocator = Nominatim(user_agent='your-app-name/1.0')

    try:
        location = geolocator.geocode(place, addressdetails=True)
        
        if location:
            target_loc = location.latitude, location.longitude
            location_data = location.raw['address']
            target = {'city': location_data.get('city', ''),
                      'state': location_data.get('state', ''),
                      'country': location_data.get('country', '')}

            r=requests.get('https://get.geojs.io./')
            ipreq=requests.get('https://get.geojs.io/v1/ip.json')
            ipadd=ipreq.json()['ip']

            url='https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'
            georeq=requests.get(url)
            geodata=georeq.json()


            latitude,longitude=geodata['latitude'],geodata['longitude']
            current_latlon = latitude, longitude
            distance = great_circle(current_latlon, target_loc).kilometers
            distance = round(float(distance), 2)
            url_place = f"https://www.google.com/maps/place/{location.latitude},{location.longitude}"
            web.open(url_place)
            speak(target)
            speak(f"{place} is {distance} kilometers away from your location.")
        else:
            print(f"Location not found for: {place}")

    except Exception as e:
        print(f"Error: {e}")
    
def cl():
    r=requests.get('https://get.geojs.io./')
    ipreq=requests.get('https://get.geojs.io/v1/ip.json')
    ipadd=ipreq.json()['ip']

    url='https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'
    georeq=requests.get(url)
    geodata=georeq.json()

    speak(f"Latitude : {geodata['latitude']}")
    speak(f"Longitude : {geodata['longitude']}")
    speak(f"City : {geodata['city']}")
    speak(f"Region : {geodata['region']}")
    speak(f"Country : {geodata['country']}")
    speak(f"Timezone : {geodata['timezone']}")
    return geodata['latitude'],geodata['longitude']

def brightness(query):
    if "brightness to high" in query:
        sb.set_brightness(100)
        speak("Your brightness is set to high")

    elif "brightness to low" in query:
        sb.set_brightness('-100')
        speak("Your brightness is set to low")

    elif "brightness to medium" in query:
        sb.set_brightness(50)
        speak("Your brightness is set to medium")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    speak(f"Your pc will function upto {hour} hour {minutes} minutes")

def battery():
    battery = psutil.sensors_battery()
    speak(f"Your battery percent is {battery.percent}")

    if battery.power_plugged:
        speak("Your PC is plugged in")

    else:
        speak("Your PC is unplugged")

    convert(battery.secsleft)

def vol(query):
    if "volume up" in query:
        pyautogui.press("volumeup")
        speak("Your volume is increased")

    elif "volume down" in query:
        pyautogui.press("volumedown")
        speak("Your volume is decreased")

    elif "mute volume" in query:
        pyautogui.press("volumemute")
        speak("Your volume is muted")

def wishme():
    speak('Hello, I am Echo AI')
    hr = int(datetime.datetime.now().hour)
    if 0 <= hr < 12:
        speak("Good Morning " )
    elif 12 <= hr < 16:
        speak("Good Afternoon " )
    elif hr >= 16:
        speak("Good Evening " )
    speak('How can I help you?')

def google(query):
    speak(f"Searching {query} on google")
    pywhatkit.search(query)

def wolfram(query):
    api_key = "UQ94PG-K6X8UW4UEK" 
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)
    try:
        answer = next(requested.results).text
        return answer
    except StopIteration:
        speak("A string value is not answerable")

def news():
    apikey = "28328ef2aa4b468da20ed3e76b0531ed"
    mainurl = "https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=4ad432c899d345f6b946ed73db668cbd"
    news = requests.get(mainurl).json()
    article = news['articles']
    newsarticle = []
    for arti in article:
        newsarticle.append(arti['title'])

    for i in range(2):
        speak(newsarticle[i])
        engine.runAndWait()

def location_info_loop():
    speak("Location Search mode activated!!")
    
    while True:
        speak("Ask about a location, or say 'exit location mode' to exit.")
        location_query = listen()

        if "exit location mode" in location_query:
            speak("Location mode exited")
            break

        try:
            speak("Here's what I found:")
            location_result = wolfram(f"Information about {location_query}")
            speak(location_result)
        except:
            speak("Sorry, I couldn't retrieve information about the location.")

def general_info_loop():
    speak("General Knowledge mode activated!!")
    
    while True:
        speak("Ask a general knowledge question, or say 'exit general knowledge mode' to exit.")
        knowledge_query = listen()

        if "exit general knowledge mode" in knowledge_query or "exit" in knowledge_query:
            speak("General Knowledge mode exited")
            break

        try:
            knowledge_result = wolfram(knowledge_query)
            speak(knowledge_result)
        except:
            speak("Sorry, I couldn't find the information you requested.")


def edu():
    speak("Calculator mode activated!!")
    while True:
        speak("Ask me to calculate, or say 'exit calculator mode' to exit.")
        abc = listen()

        if "exit calculator mode" in abc or "exit" in abc:
            speak("Calculator mode exited")
            break

        abc = abc.replace("plus", "+")
        abc = abc.replace("minus", "-")
        abc = abc.replace("power", "^")
        abc = abc.replace("by", "/")
        abc = abc.replace("into", "*")

        try:
            wolfram_res = next(client.query(abc).results).text
            speak(wolfram_res)

        except:
            speak("Sorry sir, I didn't get you. Please say that again")

        engine.runAndWait()

def get_math_formula():
    speak("Math Formula mode activated!!")
    
    while True:
        speak("Ask about a mathematical formula, or say 'exit formula mode' to exit.")
        formula_query = listen()

        if "exit formula mode" in formula_query or "exit" in formula_query:
            speak("Formula mode exited")
            break

        try:
            formula_result = wolfram(f"Formula for {formula_query}")
            speak(formula_result)
        except:
            speak("Sorry, I couldn't find the formula for the specified mathematical concept.")

def dictionary_mode_loop():
    speak("Dictionary Mode activated!!")
    
    while True:
        speak("Ask the word you want to look up, or say 'exit dictionary mode' to exit.")
        word_query = listen()

        if "exit dictionary mode" in word_query or "exit" in word_query:
            speak("Dictionary mode exited")
            break

        try:
            definition = wolfram(f"Definition of {word_query}")
            speak(definition)
        except:
            speak("Sorry, I couldn't find the definition of the word.")


def youtube(query):
    result = "https://www.youtube.com/results?search_query=" + query
    web.open(result)
    speak("This is what i found for your search .")
    pywhatkit.playonyt(query)
    speak("This may also help you.")


def playMusic(music_path):
    pygame.init()

    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print(f"Error: {e}")

    finally:
        pygame.mixer.quit()


if __name__ == '__main__':
    music_path = "./startup.mp3"
    playMusic(music_path)
    wishme()


    while True:
        query =listen()

        # sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],["instagram","https://www.instagram.com"]]
        # for site in sites:
        #     if f"Open {site[0]}".lower() in query.lower():
        #         speak(f"Opening {site[0]} ...")
        #         webbrowser.open(site[1])
        
        if "hello" in query:
            speak("Hello , I am Echo AI")
            
        elif "how are you" in query or "how are you doing" in query or "how r u" in query:
                speak("I'm fine sir. What about you?")

        elif "fine" in query:
            speak("Good to hear that sir")

        elif "do you love me" in query:
            speak("Yes sir, Ofcourse. I Love you so much")

        elif "love you" in query:
                speak("I Love you too")

        elif "what are you doing" in query:
            speak("Nothing sir, Just setting up functions for you")

        elif "need a break" in query or "sleep" in query:
            speak("Ok sir, I'm going to sleep mode")
            speak("If you need any help, just say hey Lucy")
            exit()

        elif "volume" in query:
                vol(query)

        elif "brightness" in query:
                brightness(query)

        elif "battery" in query:
                battery()

        elif "shutdown" in query or "shut down" in query:
                shut()

        elif "restart" in query:
                res()

        elif "youtube" in query:
            query = query.replace("search", "")
            query = query.replace("on youtube", "")
            speak(f"Searching {query} on youtube")
            youtube(query)
        
        elif "google search" in query or "google" in query or "search in google" in query or "search"  in query:
            query = query.replace("google search", "")
            query = query.replace("search", "")
            query = query.replace("on google", "")
            query = query.replace("in google", "")
            query = query.replace("google", "")
            query = query.replace("search in google", "")
            google(query)
        
        elif "what time is it" in query or "what is the time" in query or "time" in query:
            p = strftime("%H")
            r = strftime("%M")
            speak("Current time is " + p + " hours " + r + " minutes")

        elif "day" in query:
            now = datetime.datetime.today().strftime("%A")
            speak("Today is " + now)

        elif "date" in query:
            g = datetime.datetime.today().strftime("%d")
            e = datetime.datetime.today().strftime("%m")
            t = datetime.datetime.today().strftime("%Y")
            speak("Today's date is " + g + " " + e + " " + t)

        elif "month" in query:
            e = datetime.datetime.today().strftime("%m")
            e=int(e)-1
            months =[ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October","November","December"]
            speak("Current month is " + months[e])

        elif "which year" in query or "year" in query:
            t = datetime.datetime.today().strftime("%Y")
            speak(f"{t}")
        
        elif "locate" in query or "navigate" in query:
            query = query.replace("locate ", "")
            query = query.replace("navigate ", "")
            speak(f"Locating {query} on maps")
            googlemaps(query)

        elif 'temperature' in query:
            term = str(query)
            term = term.replace("ok ", "")
            term = term.replace("lucy ", "")
            term = term.replace("in ", "")
            term = term.replace("what is the ", "")
            term = term.replace("temperature ", "")
            tempquery = str(term)
            if "outside" in tempquery:
                var = "Temperature in Visakhapatnam"
                a = wolfram(var)
                speak(f"{var} is {a}.")
            else:
                var1 = "Temperature in " + tempquery
                ans = wolfram(var1)
                speak(f"{var1} is {ans}.")
                
        elif "news" in query:
            news()

        elif "calculator" in query:
            edu()

        elif "formula" in query:
            get_math_formula()
        
        elif "location search mode" in query or "location mode" in query or "location mod" in query:
            location_info_loop()

        elif "location" in query:
            cl()

        elif "general knowledge mode" in query or "general knowledge" in query or "general mode" in query or "knowledge" in query:
            general_info_loop()
        
        elif "dictionary mode" in query or "dictionary" in query or "dictionary mod" in query:
            dictionary_mode_loop()
         
        else :
            speak("Sorry sir, I didn't get you. Please say that again")



