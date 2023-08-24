import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser as wb
import os
from email.message import EmailMessage
import ssl
import smtplib
import pyautogui
import psutil
from time import sleep
import requests
from newsapi import NewsApiClient
import clipboard
import random
import openai


openai.api_key = os.getenv("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")

listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#dictionary for emails with key name

def talk(text):
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        talk("Good morning")
    elif hour >=12  and hour < 18:
        talk("Good afternoon")
    elif hour >= 18 and hour < 24:
        talk("Good evening")
    talk("I am Matrix, your fast and furious AI")
    talk("how may I help you")

def take_command():  
    r= sr.Recognizer()  
    with sr.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        command = r.recognize_google(audio, language= 'en-IN')
        print(command)
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return command

time = datetime.datetime.now().strftime('%I:%M %p')

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    talk(date)
    talk(month)
    talk(year)

def flip():
    talk("Okay sir flipping a coin")
    coin = ['heads', 'tails']
    toss = []
    toss.extend(coin)
    random.shuffle(toss)
    toss = ("".join(toss[0]))
    talk("I flipped the coin and it is "+toss)
    
def weather():
    APIKEY = 'ce92b3ef40fdef834e2c66144e572ac'

    BaseURL = 'https://api.openweathermap.org/data/2.5/weather'

    talk('Which city you want to view')

    City = take_command()
    RequestURL = f'{BaseURL}?appid={APIKEY}&q={City}'
    Response = requests.get(RequestURL)

    if Response.status_code == 200:
        Data = Response.json()
        weather= Data['weather'][0]['description']
        temperature = round(Data['main']['temp'] - 273.15,2)
        sunrise = datetime.datetime.utcfromtimestamp(Data['sys']['sunrise'] + Data['timezone'])
        sunset = datetime.datetime.utcfromtimestamp(Data['sys']['sunset'] + Data['timezone'])
        print('weather summary: ',weather)
        print('The temperatur is: ',temperature,'Celsius')
        print('The sunrise time is: ',sunrise)
        print('The sunset time is: ',sunset)

        talk('weather summary: '+weather)
        talk('The temperatur is: '+str(temperature)+'Celsius')
        talk('The sunrise time is: '+str(sunrise))
        talk('The sunset time is: '+str(sunset))

    else:
        talk("Try Again")

def sendEmail(email_receiver,content):
    email_sender = 'relaxmas@gmail.com'
    email_password = 'ttpuzniokbfbro'
    
    body = """" 
    hello mail from your personal ai here
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver 
    em['subject'] = content
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("Sent...")

def sendwhatsapp(phone_no,message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')

def screenshot():
    img = pyautogui.screenshot()
    img.save("E:\\Projects\\Jarvis\\Img\\ss.png")

def cpu():
    usage = str(psutil.cpu_percent())
    talk('CPU is at'+usage)
    #battery = psutil.sensors_battery
    #talk("Battery is at")
    #talk(battery.__str__ )

def news():
    newsapi = NewsApiClient(api_key='e40e26d5d334eb4805a6b3226052d6c')
    talk("What topic you need news about")
    topic = take_command().lower()
    data = newsapi.get_top_headlines(q=topic,
                                     language = 'en',
                                     page_size = 3)
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        talk(f'{x}{y["description"]}')

    talk("that's it for now")

def text_to_speech():
    text = clipboard.paste()
    print(text)
    talk(text)

def run():
    command = take_command().lower()
    #command = word_tokenize(command)
    print(command)
    print(command)
    #ifwakeword in command:
    if 'song' in command:
        music_dir = 'E:\\Music'
        songs = os.listdir(music_dir)
        talk('playing songs')
        os.startfile(os.path.join(music_dir, songs[0]))
          # add random method for random songs 
    elif 'youtube' in command:
        talk("What should I search")
        topic = take_command()
        pywhatkit.playonyt(topic)

    elif 'coin' in command:
        flip()

    elif 'news' in command:
        news()
        
    elif 'weather' in command:
        weather()
    
    elif 'read' in command:
        text_to_speech()
    
    elif 'remember that' in command:
        talk("What should I remember")
        data = take_command()
        talk("you said to remember that"+data)
        remember = open('data.txt', 'w')
        remember.write(data)
        remember.close()
    
    elif 'do you know anything' in command:
        remember = open('data.txt','r')
        talk("You said to remember that"+remember.read())

    elif 'message' in command:
        user_name = {
            'Jarvis' : '+9189','Jarvis Jarvis' : '+9189'
        }
        try: 
            talk("To whom you want to send the message?")
            name = take_command()
            phone_no = user_name[name]
            talk("what is the message")
            message = take_command()
            sendwhatsapp(phone_no,message)
            talk("Message has been sent")
        except Exception as e:
            print(e)
            talk("Sorry, because of some issues I cannot send message")
    
    elif 'date' in command:
        dat= date()
        print(dat)
        talk("Today's date is " + str(dat))
    
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('current time is ' + time)

    elif 'video' in command:
        wb.open("youtube.com")

    elif 'anime' in command:
        wb.open("https://zoro.to/")

    elif 'google' in command:
        wb.open("google.com")

    elif 'bing' in command:
        wb.open("bing.com")

    elif 'visual' in command:
        codePath = "C:\\Users\\shubh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'open' in command:
        os.system('explorer C://{}'.format(command.replace('Open','')))

    elif 'search in chrome' in command:
        talk("What should I search")
        
        search = take_command()
        pywhatkit.search(search)

    elif 'screenshot' in command:
        screenshot()
        talk("screenshot taken!")

    elif 'cpu' in command:
        cpu()

    elif 'mail' in command:
        
        try: 
            
            talk("what should I say")
            email_receiver = 'relaxmas@gmail.com'
            content = take_command()
            sendEmail(email_receiver,content)
            talk("Email has been sent")
        except Exception as e:
            print(e)
            talk("Sorry, because of some issues I cannot send email")

    elif 'wikipedia' in command:# add or condition in who or what
        talk("Searching...")
        person = command.replace('Wikipedia',"")
        info = wikipedia.summary(person, sentences = 3)# 1 no of sentences
        talk("According to Wikipedia...")
        print(info)
        talk(info)
    
    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'logout' in command:
        os.system("shutdown -l")

    elif 'shutdown' in command:
        os.system("shutdown /s /t 1")
    
    elif 'restart' in command:
        os.system("shutdown /r /t 1")

    elif 'offline' in command:
        talk('okay thank you')
        quit()

    elif 'question' in command:
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak now:")
                r.pause_threshold = 1
                audio = r.listen(source)
            try:
                print("Recognizing....")
                prompt = r.recognize_google(audio, language="en-EN", show_all=False)
                print("You asked:", prompt)
                response = openai.Completion.create(
                    # model="gpt-3.5-turbo",
                    engine="text-davinci-003",
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=300
                )
                response_text = str(response['choices'][0]['text']).strip('\n\n')
                print(response_text)
                engine.say(response_text)
                engine.runAndWait()
                print()
            except:
                response_text = "Sorry, I didn't get that!"
                print(response_text)
                engine.say(response_text)
                engine.runAndWait()
                print()
            if 'program' in prompt:
                prompt = prompt.replace("program",'')
                talk("thank you")
                break

            if 'offline' in prompt:
                prompt = prompt.replace("offline",'')
                talk("thank you")
                quit()

    else:
        talk("say again")
if __name__ == "__main__":
        #wakword = "Matrix"
    wishme()
    while True:
        run()