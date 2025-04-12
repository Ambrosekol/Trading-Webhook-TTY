from gtts import gTTS
from io import BytesIO
import pygame
import threading
import pyttsx3

def play_audio(mp3_fp):
    # Initialize pygame mixer to play audio
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        continue

def offline_speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Generate speech and play asynchronously
def speak(text):
    try:
        mp3_fp = BytesIO()
        tts = gTTS(text, lang='en', tld='co.uk', slow=False)  # Set slow=False for faster generation
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        threading.Thread(target=play_audio, args=(mp3_fp,)).start()
        
    except Exception as e:
        print(f"gTTS failed: {e}. Switching to offline TTS.")
        threading.Thread(target=offline_speak, args=(text,)).start()


