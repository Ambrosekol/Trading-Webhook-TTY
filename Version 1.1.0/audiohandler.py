from gtts import gTTS
from io import BytesIO
import pygame
import threading

def play_audio(mp3_fp):
    # Initialize pygame mixer to play audio
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        continue

# Generate speech and play asynchronously
def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='en', tld='co.uk', slow=False)  # Set slow=False for faster generation
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    threading.Thread(target=play_audio, args=(mp3_fp,)).start()


