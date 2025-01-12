import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
# print(voices[1].id)
engine.setProperty("voice", "voices[0].id")

def speak(audio):
    engine.say(audio) 
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
        
    elif hour >= 12 and hour < 18:
          speak("Good Afternoon!")
        
    else:
        speak(speak("Good Evening!"))

    speak("I am Project number 1 Sir and or Ma'am. Please tell me how i may help you?")

def takeCommand():
    #it takes microphone input from the user and returns a string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)


    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")


    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login('yourEmail@gmail.com', 'password')
    server.sendmail('yourEmail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
        
        #logic for executing tasks aed on query
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            
            
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.patch.join(music_dir, songs[0]))
            
        elif 'The time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir and or Ma'am, The time is {strTime}")
            
        elif 'open code' in query:
            codePath = "C:\\Users\\Ot\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code"
            os.startfile(codePath)
            
        elif 'email to OT' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = "OTyourEmail@gmail.com"
                sendEmail(to, content)
                speak("Email has een sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend OT shame. I am not able to send this email")