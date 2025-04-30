import sounddevice as sd
import numpy as np
import speech_recognition as sr
import webbrowser
import pyttsx3
import dicts
from scipy.io.wavfile import write
import tempfile
import os
import subprocess
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = None
browser_opened = False
screen_reader_process = None
screen_capturer_process = None

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    global screen_reader_process, screen_capturer_process
    if "play music" in c.lower():
        speak("Playing your favorite music.")
        webbrowser.open("https://open.spotify.com")  # or local folder
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = dicts.music.get(song, "")
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, song not found.")
    elif "thank you" in c.lower():
        speak("Your Welcome")
    elif any(word in c.lower() for word in ["good", "cool", "great", "awesome", "fantastic", "super"]):
        speak("Thank you Jithu")
    elif "what time is it" in c.lower():
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "what is today" in c.lower() or "what day is it" in c.lower():
        from datetime import datetime
        today = datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")
    elif "search for" in c.lower():
        global driver, browser_opened
        query = c.lower().split("search for", 1)[1]
        speak(f"Searching for {query}")
        if not browser_opened:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")
            driver = webdriver.Edge(options=options)
            browser_opened = True
        driver.execute_script(f"window.location = 'https://www.google.com/search?q={query.strip()}'")
    elif "click the first link" in c.lower() and browser_opened and driver:
        try:
            results = driver.find_elements(By.CSS_SELECTOR, "a h3")
            if results:
                first_result = results[0]
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", first_result)
                time.sleep(0.5)
                actions = ActionChains(driver)
                actions.move_to_element(first_result).pause(0.5)  # Human-like pause
                actions.click().perform()
            speak("Clicked the first link.")
        except Exception as e:
            speak("Sorry, I couldn't click the link.")
    elif "go back" in c.lower() and browser_opened and driver:
        try:
            driver.back()
            speak("Went back to the previous page.")
        except Exception as e:
            speak("Sorry, I couldn't go back.")
    elif "close browser" in c.lower() and browser_opened and driver:
        try:
            driver.quit()
            browser_opened = False
            driver = None
            speak("Closed the browser.")
        except Exception as e:
            speak("Sorry, I couldn't close the browser.")
    elif "search youtube for" in c.lower():
        query = c.lower().split("search youtube for", 1)[1]
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.strip()}")
    elif "who are you" in c.lower():
        speak("I'm your assistant, coded by the one and only Jithu!")
    elif "tell me a joke" in c.lower():
        import random
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer show up late? It had a hard drive!",
            "I told my AI it was being replaced — now it’s in denial."
        ]
        speak(random.choice(jokes))
    elif "open screen reader" in c.lower():
        if screen_reader_process is None:
            screen_reader_process = subprocess.Popen(["python", "Screenreader.py"])
            speak("Screen reader opened.")
        else:
            speak("Screen reader is already running.")
    elif "close screen reader" in c.lower():
        if screen_reader_process:
            screen_reader_process.terminate()
            screen_reader_process = None
            speak("Screen reader closed.")
        else:
            speak("No screen reader is running.")
    elif "open screen capture" in c.lower():
        if screen_capturer_process is None:
            screen_capturer_process = subprocess.Popen(["python", "ScreenCapturer.py"])
            speak("Screen capturer opened.")
        else:
            speak("Screen capturer is already running.")
    elif "close screen capture" in c.lower():
        if screen_capturer_process:
            screen_capturer_process.terminate()
            screen_capturer_process = None
            speak("Screen capturer closed.")
        else:
            speak("No screen capturer is running.")
    elif "open" in c.lower():
        found = False
        for name, url in dicts.website_links.items():
            if name in c.lower():
                speak(f"Opening {name}")
                webbrowser.open(url)
                found = True
                break
        if not found:
            for name, sys_cmd in dicts.apps.items():
                if name in c.lower():
                    speak(f"Opening {name}")
                    os.system(f"start {sys_cmd}")
                    found = True
                    break
        if not found:
            for name, path in dicts.file_paths.items():
                if name in c.lower():
                    speak(f"Opening {name}")
                    subprocess.Popen(['cmd', '/c', 'start', '', path], shell=True)
                    found = True
                    break
        if not found:
            speak("Sorry, I couldn't find that.")
    elif "scroll down" in c.lower():
        for _ in range(10):
            pyautogui.scroll(-50)
            time.sleep(0.1)
    elif "scroll up" in c.lower():
        for _ in range(10):
            pyautogui.scroll(50)
            time.sleep(0.1)
    elif "exit" in c.lower() or "quit" in c.lower() or "accept" in c.lower():
        speak("Goodbye Boss!")
        exit()
    else:
        speak("I didn't understand that.")

def record_audio(duration=3, samplerate=16000):
    print("Listening...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        write(temp_file.name, samplerate, audio_data)
        return temp_file.name

if __name__ == "__main__":
    speak("Hii Boss, Juno Nova here...")
    command = ""
    command1 = ""
    v=0
    while True:
        try:
            if command.lower() == "hello nova":
                if(v==0):
                    speak("Yes Boss, Good Day")
                    v+=1
                audio_path = record_audio(duration=4)
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                    command1 = recognizer.recognize_google(audio)
                    print(command1)
                    if("free me" in command1.lower()):
                        v=0
                        command = ""
                        speak("Yes Boss, Done")
                    elif(command1.lower() == "type"):
                        speak("Typing mode activated. Say 'stop typing' to exit.")
                        while True:
                            try:
                                audio_path = record_audio(duration=5)
                                with sr.AudioFile(audio_path) as source:
                                    audio = recognizer.record(source)
                                    typed_text = recognizer.recognize_google(audio)
                                    print("You said:", typed_text)

                                    if "stop typing" in typed_text.lower():
                                        speak("Typing mode deactivated.")
                                        break
                                    
                                    if "enter" in typed_text.lower():
                                        pyautogui.press("enter")

                                    pyautogui.write(typed_text, interval=0.05)

                                os.remove(audio_path)

                            except sr.UnknownValueError:
                                print("")
                            except Exception as e:
                                print("Error:", e)
                    else:
                        processcommand(command1)
            else:
                print("Recognizing wake word...")
                audio_path = record_audio(duration=3)
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                    command = recognizer.recognize_google(audio)
                    print(command)

            os.remove(audio_path)
        except KeyboardInterrupt:
                speak("Goodbye Boss!")
                break
        except Exception as e:
            print("")
