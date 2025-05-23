import pytesseract
from gtts import gTTS
import cv2
import os
import time
import pygame
import threading

# Global state
is_playing = False
current_audio = None
tts_lock = threading.Lock()
playback_thread = None

# Init pygame mixer
if not pygame.get_init():
    pygame.init()
pygame.mixer.init()

def narrate_slide(image):
    global is_playing, playback_thread, current_audio

    with tts_lock:
        if is_playing:
            stop_narration()
            return

        # OCR text
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, processed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(processed)

        if not text.strip():
            print("🔇 No readable content.")
            return

        # Unique filename
        timestamp = int(time.time() * 1000)
        audio_file = f"narration_{timestamp}.mp3"
        current_audio = audio_file

        print("🗣️ Generating speech...")
        try:
            tts = gTTS(text=text)
            tts.save(audio_file)
        except Exception as e:
            print("❌ Error saving TTS:", e)
            return

        print("🔊 Playing narration...")
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            is_playing = True

            def monitor_playback():
                global is_playing, current_audio
                try:
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                finally:
                    is_playing = False
                    try:
                        if current_audio and os.path.exists(current_audio):
                            os.remove(current_audio)
                    except:
                        pass
                    print("✅ Narration finished.")

            playback_thread = threading.Thread(target=monitor_playback, daemon=True)
            playback_thread.start()

        except Exception as e:
            print("🎵 Playback error:", e)
            is_playing = False
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except:
                pass

def stop_narration():
    global is_playing, current_audio
    if is_playing:
        print("🛑 Stopping narration...")
        try:
            pygame.mixer.music.fadeout(300)
            time.sleep(0.3)
        except Exception as e:
            print("⚠️ Fadeout error:", e)
        finally:
            is_playing = False
            try:
                if current_audio and os.path.exists(current_audio):
                    os.remove(current_audio)
            except:
                pass
