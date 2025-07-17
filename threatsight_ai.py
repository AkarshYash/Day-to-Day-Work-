# threatsight_ai.py

import streamlit as st
import requests
import openai
from fpdf import FPDF
from datetime import datetime

# === CONFIG ===
openai.api_key = "your-openai-api-key"  # Replace with your OpenAI key

# === FUNCTIONS ===

def fetch_ip_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res
    except Exception:
        return None

def summarize_threat(data):
    try:
        prompt = f"""Analyze the following threat intel data and summarize potential risks:\n\n{data}"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except:
        return "OpenAI failed to summarize."

def export_pdf(ip, info, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Threat Report for {ip}", ln=1)
    pdf.cell(200, 10, txt=f"Generated: {datetime.now()}", ln=2)

    pdf.multi_cell(0, 10, txt="\n--- IP Info ---\n")
    for k, v in info.items():
        pdf.multi_cell(0, 10, txt=f"{k}: {v}")

    pdf.multi_cell(0, 10, txt="\n--- Threat Summary ---\n")
    pdf.multi_cell(0, 10, txt=summary)

    filename = f"ThreatReport_{ip.replace('.', '_')}.pdf"
    pdf.output(filename)
    return filename

# === STREAMLIT UI ===

st.set_page_config(page_title="ThreatSight AI", layout="centered")
st.title("🛡️ ThreatSight AI - Cyber Intel Analyzer")

ip_input = st.text_input("🔎 Enter IP or Domain", placeholder="e.g. 8.8.8.8")

if st.button("Run Threat Analysis") and ip_input:
    with st.spinner("Scanning & Summarizing..."):
        ip_data = fetch_ip_info(ip_input)
        if ip_data and ip_data.get("status") == "success":
            summary = summarize_threat(ip_data)

            st.subheader("📌 IP Information")
            st.json(ip_data)

            st.subheader("🧠 Threat Summary (AI)")
            st.markdown(summary)

            if st.button("📁 Export PDF Report"):
                filename = export_pdf(ip_input, ip_data, summary)
                with open(filename, "rb") as f:
                    st.download_button(label="Download Report", data=f, file_name=filename, mime="application/pdf")
        else:
            st.error("❌ Could not fetch threat intel. Check IP/Domain.")

st.markdown("---")
st.caption("Built by Kalki ⚔️ | GPT-powered | Streamlit UI")
