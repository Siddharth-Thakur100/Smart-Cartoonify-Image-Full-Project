# app.py
import streamlit as st
from PIL import Image
import numpy as np
import io
import os
from cartoonify.classic import classic_cartoonify
from cartoonify.ai_style import ai_stylize
from cartoonify.utils import compute_ssim, color_histogram, timeit
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Cartoonify", layout="centered")

st.title("🖼️ Smart Cartoonify — Classic + AI Stylization")

uploaded = st.file_uploader("Upload an image", type=['png','jpg','jpeg'])
mode = st.radio("Mode", ["Classic (OpenCV)", "AI Style Transfer"])

# 🔹 Auto-load all available style examples
STYLE_DIR = "assets/style_examples"
style_files = {}

if os.path.exists(STYLE_DIR):
    for f in os.listdir(STYLE_DIR):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Convert filename like 'oilpaint.jpg' → 'Oilpaint'
            name = os.path.splitext(f)[0].replace("_", " ").title()
            style_files[name] = os.path.join(STYLE_DIR, f)

if mode == "AI Style Transfer":
    if not style_files:
        st.warning("⚠️ No styles found in assets/style_examples folder!")
    else:
        style_choice = st.selectbox("Choose a style", list(style_files.keys()))

if uploaded:
    content = Image.open(uploaded).convert('RGB')
    st.subheader("Original")
    st.image(content, use_container_width=True)

    if st.button("Process"):
        if mode == "Classic (OpenCV)":
            cartoon, elapsed = timeit(classic_cartoonify, np.array(content))
            st.subheader(f"Classic Cartoon (time: {elapsed:.2f}s)")
            st.image(cartoon, use_container_width=True)
        else:
            if style_files:
                style_pil = Image.open(style_files[style_choice]).convert('RGB')
                cartoon, elapsed = timeit(ai_stylize, content, style_pil)
                st.subheader(f"AI Stylized (time: {elapsed:.2f}s)")
                st.image(cartoon, use_container_width=True)
            else:
                st.error("No available styles found!")

        # 🔹 Analytics
        try:
            s = compute_ssim(np.array(content), cartoon)
            st.metric("SSIM (original vs cartoon)", f"{s:.4f}")
        except Exception:
            pass

        # 🔹 Histogram display
        hist = color_histogram(cartoon)
        fig, ax = plt.subplots()
        ax.plot(hist[0], label='R')
        ax.plot(hist[1], label='G')
        ax.plot(hist[2], label='B')
        ax.legend()
        st.pyplot(fig)

        # 🔹 Download button
        buf = io.BytesIO()
        Image.fromarray(cartoon).save(buf, format='PNG')
        st.download_button("Download result", data=buf.getvalue(), file_name="cartoonified.png")