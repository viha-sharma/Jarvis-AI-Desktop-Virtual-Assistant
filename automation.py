from datetime import datetime
import os
from pyautogui import click
from keyboard import press
from keyboard import press_and_release
from keyboard import write
from time import sleep
from notifypy import Notify
import pyttsx3
import speech_recognition as sr
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import webbrowser as web

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def Speak(audio):
    '''
    Creates an engine that uses the male voice from Microsoft's speech API.
    '''
    print(f'\033[1;3mJarvis\033[0m: {audio}')
    engine.say(audio)
    engine.runAndWait()

def TakeCommand():

    r = sr.Recognizer() #helps recognise audio

    with sr.Microphone() as source: # takes information from in-built microphone
        print('Listening...')
        r.pause_threshold = 1 #seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source,0,5)

    try: 
        print('Recognising...')
        query = r.recognize_google(audio,language='en-in') # works better than other recognisers currently.
        print(f'You: {query}\n')

    except Exception as e:
        print(e) #shows the error
        print('Say that again please...')
        return '' #none string if error occurs

    return query.lower()

def GoogleMaps(place):
    url_place ='https://www.google.com/maps/place/' + str(place)
    geolocator = Nominatim(user_agent='myGeocoder')
    location = geolocator.geocode(place, addressdetails=True)
    target_latlong = location.latitude, location.longitude
    location = location.raw['address']
    
    target = {'city':location.get('city', ''), 'state':location.get('state', ''),
                'country':location.get('country', '')}
    current_location = geocoder.ip('me')
    current_latlong = current_location.latlng
    distance = str(great_circle(current_latlong, target_latlong).km)
    distance = str(distance.split(' ', 1)[0])
    distance = round(float(distance),2)
    web.open(url=url_place)

    Speak(target)
    Speak(f'{place} is {distance} kilometers from your current location.')

def ChromeAuto(command): #user must click on the google chrome window to allow command activation

    query = str(command)

    if 'new tab' in query:

        press_and_release('ctrl + t')

    elif 'close tab' in query:

        press_and_release('ctrl + w')

    elif 'new window' in query:

        press_and_release('ctrl + n')

    elif 'history' in query:

        press_and_release('ctrl + h')

    elif 'downloads' in query:

        press_and_release('ctrl + j')

    elif 'bookmark' in query:

        press_and_release('ctrl + d')

        press('enter')

    elif 'incognito' in query:

        press_and_release('Ctrl + Shift + n')

    elif 'switch tab' in query:

        tab = query.replace("switch tab ", "")
        Tab = tab.replace("to","")
        
        num = Tab

        bb = f'ctrl + {num}'

        press_and_release(bb)

def YouTubeAuto(command): #user must click on the youtube window to allow command activation

    query = str(command)

    if 'pause video' or 'resume video' in query: #pause or resume the video

        press('space bar')

    elif 'full screen' in query: #full screen video viewing

        press('f')

    elif 'film screen' in query: # film screen video viewing

        press('t')
    
    elif 'mini player' in query: #miniplayer video viewing

        press('i')

    elif 'skip' in query: #forwards video by 10 seconds

        press('l')

    elif 'back' in query: #rewinds video by 10 seconds

        press('j')

    elif 'increase speed' in query: #increases playback speed

        press_and_release('SHIFT + .')

    elif 'decrease speed' in query: #decreases playback speed

        press_and_release('SHIFT + ,') 

    elif 'previous' in query: #go to previous video

        press_and_release('SHIFT + p')

    elif 'next' in query: #go to next video

        press_and_release('SHIFT + n')

    elif 'mute' in query: #Mutes video

        press('m')

    elif 'unmute' in query:

        press('m')

    else:
        Speak("No Command Found!")


def amazonsearch(command):

    query = str(command)

    url1 = 'https://www.amazon.in/s?k='
    query = query.replace('search amazon for', '')
    query = query.replace('search for', '')
    query = query.replace('Jarvis', '')
    query = query.replace('on amazon', '')
    query.replace(' ', "+")
    Speak('Searching on amazon...')
    web.open(url1+query) 


def WindowsAuto(command):

    query = str(command)

    if 'home screen' in query:

        press_and_release('windows + m')

    elif 'minimize' in query:

        press_and_release('windows + m')

    elif 'show start' in query:

        press('windows')

    elif 'open setting' in query:

        press_and_release('windows + i')

    elif 'open search' in query:

        press_and_release('windows + s')

    elif 'restore windows' in  query:

        press_and_release('Windows + Shift + M')

    else:
        Speak("Sorry , No Command Found!")

def Notepad():

    Speak("Grabbing my pen and paper.")
    Speak("Ok I am ready, tell me the note")

    writes = TakeCommand()

    time = datetime.now().strftime("%H:%M")

    filename = str(time).replace(":","-") + "-note.txt"

    with open(filename,"w") as file:

        file.write(writes)

    path_1 = 'C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\' + str(filename)

    path_2 = "C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\Notepad\\" + str(filename)

    os.rename(path_1,path_2)

    os.startfile(path_2)

def CloseNotepad():

    os.system("TASKKILL /F /im Notepad.exe")

def TimeTable():

    from Database.TimeTable.TimeTable import Time
    Time()