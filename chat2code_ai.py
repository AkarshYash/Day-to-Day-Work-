# chat2code_ai.py

import streamlit as st
import openai

# === SETUP ===
openai.api_key = "your-openai-key"  # Replace with your OpenAI API key

# === STREAMLIT CONFIG ===
st.set_page_config(page_title="Chat2Code AI", layout="centered")
st.title("🧠 Chat2Code AI - Natural Language to Python Code")
st.caption("Turn ideas into code instantly using GPT 🚀")

# === INPUT UI ===
prompt = st.text_area("💬 Describe your project or task (in English)", placeholder="e.g. Create a Python function to scrape headlines from a news site...")

if st.button("⚙️ Generate Code") and prompt.strip():
    with st.spinner("Generating code..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Python expert who only outputs working code without explanations."},
                    {"role": "user", "content": f"Write Python code to: {prompt}"}
                ],
                max_tokens=500,
                temperature=0.3
            )
            generated_code = response.choices[0].message.content.strip()

            st.subheader("🧩 Generated Code")
            st.code(generated_code, language="python")

            st.download_button("💾 Download Code", generated_code, file_name="generated_code.py", mime="text/x-python")

        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("Enter a prompt and click Generate to get started!")

st.markdown("---")
st.caption("🔥 Built by Kalki | GPT-powered Python dev assistant")
