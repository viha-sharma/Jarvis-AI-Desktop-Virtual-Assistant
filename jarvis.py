import datetime
import os
import webbrowser
import nltk
import pyjokes
import pyttsx3  # text to speech conversion library
import pywhatkit
import speech_recognition as sr
import wikipedia
from googlesearch import search  # installed beautifulsoup4 & google
from PyDictionary import PyDictionary
import pytube #pip install pytube, pip install os_sys
from pytube import YouTube
import pygame
import random
import requests
from pywikihow import RandomHowTo, search_wikihow
import wolframalpha
from time import sleep
import cv2
import qrcode
import pyautogui
import PyPDF2
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk import wordnet
from nltk.corpus import wordnet

engine = pyttsx3.init('sapi5') # Microsoft speech API
voices = engine.getProperty('voices') # getting the available voices

# voices[0]: David (Male)
# voices[1]: Zira (Female)

myname = 'Viha'

# setting Voice

engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180) #200 = 1x (Normal), 180=0.9x

#creating speak function

def speak(audio):
    '''
    Creates an engine that uses the male voice from Microsoft's speech API.
    '''
    print(f'\033[1;3mJarvis\033[0m: {audio}')
    engine.say(audio)
    engine.runAndWait()

def Greet():
    '''
    Greets user based on the time of day
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >=6 and hour<12:
        speak('Good Morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    elif hour>=18 and hour<22:
        speak('Good Evening!')
    else:
        speak('Hello, you are up late!')
    
    speak('I am Jarvis. How may I help you?')

def listen():
    '''
    It takes microphone input from the user and returns a string output
    '''
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
    return query

def WolfRam(query):
    '''
    adds maths and science elements to Jarvis
    '''
    api_key = "U2V5E5-G6GGQEPLWV"
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer

    except:
        speak('Oops, no data found')

def calculator(query):
    '''
    Uses wolfram API to do arithmetic operations
    '''
    term = str(query)
    term = term.replace('jarvis', '')
    term = term.replace('multiplied by', '*')
    term = term.replace('into', '*')
    term = term.replace('plus', '+')
    term = term.replace('minus', '-')
    term = term.replace('divided by', '/')
    term = term.replace('what is', '')
    term = term.replace('to the power', '**')
    final = str(term)

    try:
        result = WolfRam(final)
        speak(result)
    except:
        speak('Sorry, I could not calculate this')

def temp(query):
    '''
    Uses Wolfram API to get temperature details for any place in the world
    '''
    temp =  str(query)
    temp = temp.replace('jarvis ', '')
    temp = temp.replace('what is the ', '')
    temp = temp.replace('temperature ', '')
    temp = temp.replace('in ', '')

    temp_query = str(temp)

    if 'home' in temp_query:

        var1 = 'temperature in delhi'
        answer = WolfRam(var1)
        speak(f'The temperature outside is {answer}')

    else:

        var2 = 'temperature in ' + temp_query
        answer1 = WolfRam(var2)
        speak(f'the {var2} is {answer1}')

def thesaurus():
    '''
    Provides synonyms for a word taken as user input
    '''
    synonyms = []
    speak('Please enter the word in my terminal')
    query = str(input('Enter a word: '))

    for syn in wordnet.synsets(query):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    speak('The synonyms of {} are'.format(query))
    speak(synonyms[:5])
    speak('Would you like to hear more synonyms?')
    reply_synonym = listen()
    if 'yes' in reply_synonym:
        speak(synonyms[5:10])
    else:
        speak('Okay.')

def My_Location():
    '''
    Uses ip address to detect where the user is located
    '''
    ip_add = requests.get('https://api.ipify.org').text 
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    city = geo_d['city']
    country = geo_d['country']
    speak(f'Currently, you are in {city, country}')

def coin_sound():
    '''
    plays the sound of a coin being tossed
    '''
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\Sounds\\coins.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(60)

def dice_roll_sound():
    '''
    plays the sound of a dice being rolled
    '''
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\Sounds\\dice.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(10)

def pdf_reader():
    '''
    Reads any pdf document, provided that it is located in the PDF files folder in the database
    '''
    speak("Enter the name of the pdf that you want to read")
    n = input("Enter the pdf name: ")
    n = n.strip()+".pdf"
    book_n = open(f'C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\PDF Files\\{n}','rb')
    pdfReader = PyPDF2.PdfFileReader(book_n)
    pages = pdfReader.numPages
    speak(f"Boss there are total of {pages} pages in this pdf")
    speak("please enter the page number that I need to read")
    num = int(input("Enter the page number: "))
    page = pdfReader.getPage(num)
    text = page.extractText()
    print(text)
    speak(text)

def qrCodeGenerator():
    '''
    Generates a personalised QR code for any link
    '''
    speak(f"Please enter the text/link that you want to keep in the qr code")
    input_Text_link = input("Enter the Text/Link : ")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    QRfile_name = (str(datetime.datetime.now())).replace(" ","-")
    QRfile_name = QRfile_name.replace(":","-")
    QRfile_name = QRfile_name.replace(".","-")
    QRfile_name = QRfile_name+"-QR.png"
    qr.add_data(input_Text_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\QRCodes\\{QRfile_name}')
    speak(f"Your personalised qr code has been generated, it is located in the QR Codes folder.")

def rap_god():
    '''
    Jarvis can sing Rap God by Eminem
    '''
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\Sounds\\Chatbot rap god.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(50)  

def webCam(): #Note: to exit from the web camera press "ESC" key   
    '''
    Opens the webcam and quits
    '''
    speak('Opening camera')
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('web camera',img)
        k = cv2.waitKey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    exit()

def screenshot():
    '''
    Jarvis takes a screenshot and saves it to the screenshot folder in the database
    '''
    speak("Please tell me the name for this screenshot file")
    name = listen()
    speak("Ok, hold the screen for a few seconds, I am taking the screenshot")
    sleep(3)
    img = pyautogui.screenshot()
    img.save(f"C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Screenshots\\{name}.png")
    speak("Screen captured successfully, access the image from the screenshots folder.")

if __name__ == "__main__":
    Greet()
    
    while True:
    
        query = listen().lower()

    #logic for executing tasks based on query

        if 'wikipedia' in query: #Try saying: Search Wikipedia for Jeff Bezos
            speak('Searching Wikipedia')
            query = query.replace('search', '')
            query = query.replace('wikipedia', "")
            query = query.replace('for;','')
            results = wikipedia.summary(query, sentences =2)
            speak('According to Wikipedia')
            speak(results)

        elif 'open youtube' in query: #opens youtube in the browser
            webbrowser.open('youtube.com')

        elif 'how to' in query: #searches wikihow and provides steps to achieve anything provided in the query
            how_to_func = search_wikihow(query=query, max_results=1)
            assert len(how_to_func) == 1
            how_to_func[0].print()
            speak(how_to_func[0].summary)

        elif 'i need to buy' in query: #opens myntra for online shopping - provide a product category eg:red shoes
            query = query.replace('i need to buy', '')
            query = query.replace('jarvis', '')
            query = query.replace('search for', '')
            query = query.replace('on', '')
            query = query.replace('myntra', '')
            query = query.replace(' ', '+')
            webbrowser.open(f'myntra.com/{query}')
            speak('In that case, you should consider these products')
            exit()

        elif 'search amazon for' in query:
            from automation import amazonsearch
            amazonsearch(query)
            exit()

        elif 'my location' in query:
            My_Location()

        elif 'where is' in query: #Try saying: Jarvis where is Mumbai, it will tell you how far the place is from your location
            place = query.replace('where is', '')
            place = place.replace('jarvis', '')
            from automation import GoogleMaps
            GoogleMaps(place)
        
        elif 'news' in query: #Gives the top 10 headlines for the day
            from news_auto import news
            news()

        elif 'teach me something new' in query: #Learn a new skill/topic everyday with a step by step guide using wikihow
            random_wiki = RandomHowTo()
            speak(random_wiki.summary)
 
        elif 'open stack overflow' in query: #opens stackoverflow
            webbrowser.open('stackoverflow.com')

        elif 'open netflix' in query: #opens netflix
                speak('I\'ll grab the popcorn!')
                webbrowser.open('netflix.com')

        elif 'kya hal hai' in query: #replying in hindi to a question asked in hindi
            speak('theek hu! tum kaise ho?')

        elif 'mei bhi theek hu' in query: 
            speak(f'Badiya. What can I do for you today {myname}')

        elif 'namaste' in query: #hindi greeting
            speak('namaste')
        
        elif 'what is my name' in query: #Jarvis can remember your name
            speak(f'Your name is {myname}')

        elif 'change my name' in query:
            speak('What do you want me to call you?') #Jarvis will change your name 
            myname = listen()
            myname = myname.replace('call me', '')
            speak(f'ok, from now i will call you {myname}')

        elif 'what can you do' in query:
            speak('''I can perform 50+ actions that will automate your day to day online activities. Some of these are:
            1. Opening web pages like google, stack overflow and youtube.
            2. Opening local applications such as powerpoint, excel and webcam
            3. Reading a PDF to you
            4. Telling you todays news
            5. Dictionary word meanings
            6. Synonyms of words
            7. Automating your reminders 
            8. Telling you todays schedule
            9. Taking screenshots
            10. Creating personalised qr codes
            11. Automating online shopping at amazon and myntra
            12. Performing arithmetic calculations
            13. Automating youtube actions
            14. Telling you jokes
            15. Currency conversion
            16. Flip a coin or roll a dice
            17. Teaching you something new''')

        elif 'screenshot' in query: #Takes a screenshot and saves it in the database
            screenshot()

        elif 'who created you' in query: #Background information 
            speak('I was created by Viha Sharma in November 2022.')

        elif 'hi jarvis' in query: #greetings
            speak(f'Hello {myname}. How are you today?')

        elif 'Who are you' in query:
             speak('I am Jarvis and I will be at your service 24 7!')   

        elif 'how are you' in query: #greetings
            speak(f'Better, now that you are here {myname}')
            speak('What can I do for you today?')

        elif 'temperature' in query: 
            temp(query)

        elif 'calculate' in query:
            calculator(query)

        elif 'on google' in query: #opens google search results 
            url = 'https://www.google.com/search?q='   #Search Query Url
            query = query.replace('search', '')
            query = query.replace('search for', '')
            query = query.replace('on google', '')
            speak(f'Searching on Google...')
            webbrowser.open(url+query)

        elif 'open webcam' in query:
            webCam()

        elif 'chrome' in query: #automates chrome: new tab, close tab, history, downloads, make a bookmark, switching tabs, incognito mode
            from automation import ChromeAuto
            ChromeAuto(query)

        elif 'control youtube' in query: #automates youtube: pause, resume, full screen, film screen, increase/decrease playback speed, etc
            from automation import YouTubeAuto
            YouTubeAuto(query) #try saying: control youtube pause video or control youtube full screen

        elif 'currency convertor' in query: #converts currency (INR, USD, CAD, EUR, CNY, DKK) to another using Tkinter
            import currency_convertor
            currency_convertor     

        elif 'write a note' in query: # writes a note and saves it in database
            from automation import Notepad
            Notepad()

        elif 'close notepad' in query: #closes notepad
            from automation import CloseNotepad
            CloseNotepad()

        elif 'remember that' in query: #setting reminders
            remembermsg = query.replace('remember that', '')
            remembermsg = remembermsg.replace('jarvis', '')
            speak(f'Reminder set: {remembermsg}')
            remember = open('reminders.txt', 'w')
            remember.write(remembermsg)
            remember.close()

        elif 'what are my reminders' in query: #checking reminders
            remember = open('reminders.txt', 'r')
            if os.stat("reminders.txt").st_size == 0:
                speak('You have not set any reminders yet.')
            else:
                speak('You told me that:'+ remember.read())

        elif 'clear reminders' in query: #clearing all reminders 
            f = open('reminders.txt', 'r+')
            f.truncate(0) # need '0' when using r+
            f.close()
            speak('Cleared all reminders.')

        elif 'time table' in query: #tells you your schedule based on the current time of the day
            from automation import TimeTable
            TimeTable()
        
        elif 'on youtube' in query: #performs a youtube search
            url = 'https://www.youtube.com/results?search_query='
            query = query.replace('on youtube', '')
            query = query.replace('jarvis', '')
            query = query.replace('search for', '')
            query.replace(' ', "+")
            speak('Opening Youtube...')
            webbrowser.open(url+query)

        elif 'control windows' in query: #automates windows functions such as 
            from automation import WindowsAuto
            WindowsAuto(query)

        elif 'qr code' in query: #generates personalised qr code and saves it to the database
                qrCodeGenerator()

        elif ('play the song' or 'play') in query: #plays music on youtube
             url = 'https://www.youtube.com/results?search_query='
             query1 = query.replace('on youtube', '')
             query1 = query1.replace('play the song', " ")
             query1 = query1.replace('open', " ")
             speak('Opening Youtube...')
             pywhatkit.playonyt(query)

        elif 'open excel' in query: #opens excel
            excelpath = "C:\\Program Files\\Microsoft Office\\root\Office16\\EXCEL.EXE"
            speak('I hope you have an EXCEL-lent day')
            os.startfile(excelpath)

        elif 'open powerpoint' in query: #opens powerpoint
            pptpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
            speak('Why did the chicken cross the PowerPoint? To get to the other slide')
            os.startfile(pptpath)

        elif 'open word' in query: #opens microsoft word
            pptpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            speak('Opening Microsoft Word...')
            os.startfile(pptpath)

        elif 'open my sql workbench' in query:
            sqlpath = "C:\\Program Files\\MySQL\\MySQL Workbench 8.0\\MySQLWorkbench.exe"
            speak('Opening mySQL Workbench')
            os.startfile(sqlpath)

        elif 'the time' in query: #tells the current time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'The time is {strTime}')

        elif 'read pdf' in query: #reads a pdf stored in the database
            pdf_reader()      

        elif 'late for class' in query: #takes you to the niit online program portal
            speak('Hop on! Let me teleport you to class!')
            webbrowser.open('https://www.niit.com/india/')

        elif 'open thesaurus' in query: #
            thesaurus()
            exit()

        elif 'flip a coin' in query: #flips a coin
            coin_sound()
            speak(random.choice(['tails','heads']))

        elif 'dice roll' in query:
            dice_roll_sound()
            speak(random.choice([1,2,3,4,5,6]))

        elif 'joke' in query: #tells a random programming joke
            speak(pyjokes.get_joke())
            speak('I have many more up my sleeves. Care to hear another?')
            reply = listen()
            if 'yes' in reply:
                speak(pyjokes.get_joke())
            else:
                speak('Hope you had a laugh!')

        elif 'what is the spelling of' in query: #tells spelling of a word
            query = query.replace('jarvis ', '')
            query = query.replace('what is the spelling of ','')
            speak(f'the spelling of {query} is')
            for i in query:
                speak(i)
            
        elif 'what is the meaning of' in query: #tells the meaning of a word
            dictionary = PyDictionary()
            query = query.replace('what is the meaning of', '')
            speak(dictionary.meaning(query))
            
        elif 'can you rap' in query: #sings rap god by Eminem
            speak('Some call me.. Rap god')
            rap_god()
            sleep(100)

        elif 'video to mp3' in query: #converts a youtube video to mp3, and saves it to a folder on the desktop
            speak('Understood. Please enter the URL of the video you wish to download in my terminal')
            yt = YouTube(str(input("Enter the URL of the video you want to download: \n>> ")))
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path='C:\\Users\\Viha\\Desktop\\Jarvis AI Desktop Voice Assistant\\Database\\youtube_to_mp3')
            base, ext = os.path.splitext(out_file)    
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

            speak(yt.title + " has been successfully downloaded.")
            speak('You can access it from the youtube to mp3 folder on your desktop')

        elif 'quit' in query: # quits 
            speak('Jarvis out.')
            exit()

        elif 'thank you' in query: # quits
            speak('happy to help!')
            exit()

        elif 'finger on the lips' in query: #silent quit
            exit()   
