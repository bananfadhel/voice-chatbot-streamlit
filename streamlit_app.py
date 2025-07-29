import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

def transcribe(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()
        with sr.AudioFile(temp_audio.name) as source:
            audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Sorry, I couldn't understand."

def respond(text):
    text = text.lower()
    if "hello" in text:
        return "Hello! How can I help you?"
    elif "name" in text:
        return "I'm your voice chatbot!"
    elif "how are you" in text:
        return "I'm doing great!"
    elif "bye" in text:
        return "Goodbye!"
    else:
        return "I didn't quite understand that."

def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# واجهة Streamlit
st.title("🎙️ Voice Chatbot (Streamlit)")

audio_data = mic_recorder(start_prompt="🎤 Click to talk", stop_prompt="⏹️ Stop", just_once=True, key='listen')

if audio_data:
    st.audio(audio_data['bytes'], format='audio/wav')
    user_text = transcribe(audio_data['bytes'])
    st.markdown(f"**You said:** {user_text}")
    bot_reply = respond(user_text)
    st.markdown(f"**Bot says:** {bot_reply}")
    tts_file = speak(bot_reply)
    st.audio(tts_file, format="audio/mp3")
