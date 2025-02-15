import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

translation_active = False
translator = Translator() 
pygame.mixer.init() 
language_codes = {name: code for code, name in LANGUAGES.items()}

def fetch_language_code(language_name):
    return language_codes.get(language_name, language_name)

def perform_translation(input_text, source_lang, target_lang):
    return translator.translate(input_text, src=source_lang, dest=target_lang)

def convert_text_to_speech(text_content, language_code):
    audio_object = gTTS(text=text_content, lang=language_code, slow=False)
    audio_object.save("temp_audio.mp3")
    sound = pygame.mixer.Sound("temp_audio.mp3")  
    sound.play()
    os.remove("temp_audio.mp3")

def process_translation(status_holder, result_holder, source_lang, target_lang):
    global translation_active
    
    conversation_log = []

    while translation_active:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            status_holder.text("Listening...")
            recognizer.pause_threshold = 1
            audio_input = recognizer.listen(source, phrase_time_limit=10)
        

        
        try:
            status_holder.text("Processing...")
            recognized_text = recognizer.recognize_google(audio_input, language=source_lang)
            
            status_holder.text("Translating...")
            translated_result = perform_translation(recognized_text, source_lang, target_lang)








            convert_text_to_speech(translated_result.text, target_lang)
            conversation_log.append((recognized_text, translated_result.text))
            result_holder.text("\n".join([f"Spoken: {orig}\nTranslated: {trans}" for orig, trans in conversation_log]))
        except Exception as error:
            status_holder.text(f"Error: {str(error)}")
st.title("Language Translator")
source_language = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
target_language = st.selectbox("Select Target Language:", list(LANGUAGES.values()))
source_lang_code = fetch_language_code(source_language)
target_lang_code = fetch_language_code(target_language)
begin_translation = st.button("Start")
end_translation = st.button("Stop")
status_holder = st.empty()
result_holder = st.empty()
if begin_translation:
    if not translation_active:
        translation_active = True
        process_translation(status_holder, result_holder, source_lang_code, target_lang_code)
if end_translation:
    translation_active = False

