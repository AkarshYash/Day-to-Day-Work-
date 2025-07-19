# autocolorizer_ai.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os

# Load model files
PROTOTXT = "models/colorization_deploy_v2.prototxt"
CAFFEMODEL = "models/colorization_release_v2.caffemodel"
POINTS = "models/pts_in_hull.npy"

def load_model():
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFEMODEL)
    pts = np.load(POINTS)
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [pts.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    return net

def colorize(img, net):
    img = np.array(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2LAB)
    img_resized = cv2.resize(img_lab, (224, 224))
    
    L = img_resized[:, :, 0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (img.shape[1], img.shape[0]))
    
    L_orig = img_lab[:, :, 0]
    colorized = np.concatenate((L_orig[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized.astype("float32"), cv2.COLOR_LAB2RGB)
    colorized = np.clip(colorized, 0, 1)
    return (colorized * 255).astype("uint8")

# --- UI ---
st.set_page_config(page_title="AutoColorizer AI")
st.title("🎨 AutoColorizer AI - B&W to Color Image")

st.markdown("Upload a grayscale image and let AI colorize it 🌈")

uploaded_file = st.file_uploader("🖼️ Upload Black & White Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Grayscale Image", use_column_width=True)

    if st.button("🧠 Colorize"):
        with st.spinner("Colorizing..."):
            model = load_model()
            result = colorize(image, model)
            st.image(result, caption="🟩 Colorized Image", use_column_width=True)
            st.success("Done!")

            img_download = Image.fromarray(result)
            st.download_button("📥 Download Colorized Image", img_download.tobytes(), file_name="colorized.png", mime="image/png")

st.markdown("---")
st.caption("Built with OpenCV + Streamlit + AI ❤️‍🔥")
