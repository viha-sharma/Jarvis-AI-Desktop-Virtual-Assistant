from newsapi import NewsApiClient
api_key = 'fd6c364ed9c34eedaa7232e60216deff'
from requests import get
import pyttsx3
import speech_recognition as sr

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


def news():
    MAIN_URL_= f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}"
    MAIN_PAGE_ = get(MAIN_URL_).json()
    articles = MAIN_PAGE_["articles"]
    headings=[]
    seq = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'] #If you need more than ten you can extend it in the list
    for ar in articles:
        headings.append(ar['title'])
    for i in range(len(seq)):
        Speak(f"todays {seq[i]} news is: {headings[i]}")
    Speak("You are now up to date!")

news()