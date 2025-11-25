import streamlit as st
import pandas as pd
import random
import base64
from io import BytesIO

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Chia Đội Thể Thao", layout="wide")

# ======================
# BACKGROUND IMAGE SETUP
# ======================

DEFAULT_BG_PATH = "/mnt/data/A_high-resolution_photograph_captures_four_fit_wom.png"

def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.sidebar.header("🎨 Tuỳ chỉnh giao diện")
uploaded_bg = st.sidebar.file_uploader("Tải hình nền (tùy chọn)", type=["jpg", "jpeg", "png"])

if uploaded_bg:
    bg_data = uploaded_bg.read()
    bg_base64 = base64.b64encode(bg_data).decode()
else:
    bg_base64 = load_image_base64(DEFAULT_BG_PATH)

# --- CSS (Blur + dark overlay mạnh) ---
page_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
}}

[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    backdrop-filter: blur(16px);
    background: rgba(0, 0, 0, 0.55);
    z-index: 0;
}}

.block-container {{
    position: relative;
    z-index: 5;
}}
