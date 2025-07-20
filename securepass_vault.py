# securepass_vault.py

import streamlit as st
import openai
import os
import json
from cryptography.fernet import Fernet
from datetime import datetime

# === CONFIG ===
openai.api_key = "your-openai-key"  # Replace this with your OpenAI API key
VAULT_FILE = "vault.json"
KEY_FILE = "secret.key"

# === SECURITY ===
def generate_key(master_password):
    return Fernet(Fernet.generate_key())

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return Fernet(f.read())
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return Fernet(key)

fernet = load_or_create_key()

def save_password(site, password):
    vault = {}
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            vault = json.load(f)

    encrypted_pass = fernet.encrypt(password.encode()).decode()
    vault[site] = {"password": encrypted_pass, "saved": str(datetime.now())}

    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=2)

def get_vault():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}

# === AI-POWERED GENERATOR ===
def generate_password(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Generate a secure password based on: {prompt}. Just the password, no explanation."}
            ],
            temperature=0.6,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# === STREAMLIT UI ===
st.set_page_config(page_title="SecurePass Vault", layout="centered")
st.title("🔐 SecurePass Vault - AI Password Manager")

tab1, tab2, tab3 = st.tabs(["🔧 Generate", "📥 Vault", "📤 Save Password"])

# === GENERATE TAB ===
with tab1:
    st.subheader("AI-Powered Password Generator")
    prompt = st.text_input("Describe your password need:", placeholder="e.g. 16 char, special symbols, for Gmail")
    if st.button("🧠 Generate"):
        pwd = generate_password(prompt)
        st.code(pwd, language="text")
        st.success("You can copy and save it below.")

# === SAVE TAB ===
with tab3:
    st.subheader("Save to Local Vault")
    site = st.text_input("🔖 Site/App Name")
    password = st.text_input("🔑 Password", type="password")
    if st.button("💾 Save Password"):
        save_password(site, password)
        st.success(f"Password for {site} saved securely!")

# === VAULT TAB ===
with tab2:
    st.subheader("Your Vault")
    vault = get_vault()
    if vault:
        for site, data in vault.items():
            st.write(f"🔐 **{site}** (saved: {data['saved']})")
            if st.button(f"👁️ View {site}", key=site):
                decrypted = fernet.decrypt(data['password'].encode()).decode()
                st.code(decrypted, language="text")
    else:
        st.info("Vault is empty.")

st.markdown("---")
st.caption("Built by Kalki 🧠🔐 | Offline Vault + AI Secure Generator")
