import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import configparser
from spotipy.oauth2 import SpotifyOAuth

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis . Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  
        print("Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)  
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    try:
        config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_file)

        email_address = config['EMAIL']['ADDRESS']
        email_password = config['EMAIL']['PASSWORD']

        print(f"Sending email from: {email_address}")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to, content)
        server.close()

        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the email server. Check your email address and password.")
        speak("Failed to authenticate with the email server.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        speak("An SMTP error occurred.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An error occurred while sending the email.")


def open_spotify_and_play():
    spotify_link = "https://open.spotify.com/track/7dJYggqjKo71KI9sLzqCs8?si=78e100a18a214696"
    webbrowser.open(spotify_link)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.PageError as e:
                speak("I could not find any relevant information.")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("https://www.stackoverflow.com")
        elif 'play music' in query:
            open_spotify_and_play()
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'Open VS Code' in query:
            codePath = "C:\\Users\\BALE RAM\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'send mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "knav12mna@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            
            except Exception as e:
                print(f"Error: {str(e)}")
                speak("I am not able to send this email right now.")

