
Project -  C++ - Python  - Bash  - Web Work - GUI


smartassist_ai.py
import streamlit as st
import openai
import sqlite3
import datetime
import speech_recognition as sr
from textblob import TextBlob
import os

# ==== SETUP ====
openai.api_key = "YOUR_OPENAI_API_KEY"

conn = sqlite3.connect("smartassist.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    date TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry TEXT,
    mood TEXT,
    date TEXT
)""")

# ==== AI CHAT ====
def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# ==== VOICE TO TEXT ====
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... 🎙️")
        audio = r.listen(source, timeout=5)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Couldn't understand the audio"
        except sr.RequestError:
            return "Voice recognition service error"

# ==== TASK MANAGEMENT ====
def add_task(task, date):
    cursor.execute("INSERT INTO tasks (task, date) VALUES (?, ?)", (task, date))
    conn.commit()

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

# ==== JOURNAL + MOOD ====
def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "Positive"
    elif polarity < -0.3:
        return "Negative"
    else:
        return "Neutral"

def add_journal(entry, mood):
    date = str(datetime.date.today())
    cursor.execute("INSERT INTO journal (entry, mood, date) VALUES (?, ?, ?)", (entry, mood, date))
    conn.commit()

def get_journals():
    cursor.execute("SELECT * FROM journal ORDER BY date DESC")
    return cursor.fetchall()

# ==== STREAMLIT UI ====
st.set_page_config(page_title="SmartAssist AI", layout="centered")
st.title("🧠 SmartAssist AI — All-in-One Daily Assistant")

menu = st.sidebar.selectbox("Choose", ["AI Chat", "Task Planner", "Mood Journal", "Voice Input"])

# === AI CHAT ===
if menu == "AI Chat":
    st.subheader("🤖 Chat with your assistant")
    user_input = st.text_input("Ask something...")
    if st.button("Ask"):
        response = ask_ai(user_input)
        st.success(response)

# === TASK PLANNER ===
elif menu == "Task Planner":
    st.subheader("📅 Add Daily Task")
    task = st.text_input("Task")
    date = st.date_input("Date", datetime.date.today())
    if st.button("Add Task"):
        add_task(task, str(date))
        st.success("Task added!")

    st.markdown("### 📝 Your Tasks")
    tasks = get_tasks()
    for t in tasks:
        st.write(f"✅ {t[1]} — 📅 {t[2]}")

# === MOOD JOURNAL ===
elif menu == "Mood Journal":
    st.subheader("😴 Write Journal")
    journal_entry = st.text_area("How are you feeling today?")
    if st.button("Analyze Mood"):
        mood = analyze_mood(journal_entry)
        add_journal(journal_entry, mood)
        st.success(f"Logged with mood: **{mood}**")

    st.markdown("### 📔 Past Entries")
    for j in get_journals():
        st.info(f"{j[3]} — {j[2]}\n{j[1]}")

# === VOICE INPUT ===
elif menu == "Voice Input":
    st.subheader("🎙️ Talk to SmartAssist")
    if st.button("Start Listening"):
        transcript = voice_input()
        st.text_area("Transcription:", transcript)
        if st.button("Ask AI with Voice"):
            st.success(ask_ai(transcript))

st.markdown("---")
st.caption("Built by Kalki ✨")
