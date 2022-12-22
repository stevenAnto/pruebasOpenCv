#requiere pyaudio, installar python -m pip install pyaudio en windons

import speech_recognition as sr
def callback(recognizer, audio):                          # this is called from the background thread
    try:
        print("You said......................................... "+recognizer.recognize_google(audio,language='es'))  # received audio data, now need to recognize it
    except LookupError:
        print("Oops! Didn't catch that")
r = sr.Recognizer()
m = sr.Microphone()
r.listen_in_background(m, callback)

import time
while True:time.sleep(0.1)


