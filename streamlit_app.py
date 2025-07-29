import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from gtts import gTTS
import tempfile
import base64
import os

def transcribe(audio_bytes):
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio.flush()
            temp_filename = temp_audio.name
        with sr.AudioFile(temp_filename) as source:
            audio = recognizer.record(source)
        os.remove(temp_filename)  # حذف الملف المؤقت بعد الاستخدام
        return recognizer.recognize_google(audio)
    except Exception as e:
        return f"Sorry, I couldn't understand. Error: {e}"

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

audio_data = mic_recorder(
    start_prompt="🎤 Click to talk",
    stop_prompt="⏹️ Stop",
    just_once=True,
    key='listen'
)

if audio_data:
    # لو البيانات اللي ترجعها base64 بدل bytes، حولها bytes
    if isinstance(audio_data['bytes'], str) and audio_data['bytes'].startswith("data:audio"):
        header, encoded = audio_data['bytes'].split(",", 1)
        audio_bytes = base64.b64decode(encoded)
    else:
        audio_bytes = audio_data['bytes']

    st.audio(audio_bytes, format='audio/wav')

    user_text = transcribe(audio_bytes)
    st.markdown(f"**You said:** {user_text}")

    bot_reply = respond(user_text)
    st.markdown(f"**Bot says:** {bot_reply}")

    tts_file = speak(bot_reply)
    st.audio(tts_file, format="audio/mp3")

    # حذف ملف الصوت بعد العرض (اختياري)
    if os.path.exists(tts_file):
        os.remove(tts_file)

