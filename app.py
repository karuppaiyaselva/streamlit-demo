import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import tempfile
import os
import time

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)
        
        try:
            speech_text = recognizer.recognize_google(audio)
            return speech_text
        except sr.UnknownValueError:
            st.error("Could not understand the speech.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition.")
        except Exception as e:
            st.error(f"Error: {e}")
    return None

def translate_text(text, target_language='ta'):
    try:
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

def text_to_speech(text, lang='ta'):
    try:
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_file = temp_audio.name
        temp_audio.close()

        voice = gTTS(text=text, lang=lang, slow=False)
        voice.save(audio_file)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        time.sleep(1)  # Allow time for pygame to fully release the file
        os.remove(audio_file)  # Delete the file safely

    except Exception as tts_error:
        st.error(f"gTTS Error: {tts_error}")

# Streamlit UI
st.title("Speech Translation App")
st.write("Speak in any language, and we'll translate it to Tamil and play the audio!")

if st.button("Start Recording"):
    speech_text = recognize_speech()
    
    if speech_text:
        st.success(f"You said: {speech_text}")
        translated_text = translate_text(speech_text, target_language='ta')
        
        if translated_text:
            st.success(f"Translated: {translated_text}")
            text_to_speech(translated_text, lang='ta')
