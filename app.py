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
# BACKGROUND IMAGE FROM UPLOADED FILE (KHÔNG CẦN LƯU FILE TRONG PROJECT)
# ======================

BG_PATH = "/mnt/data/hinh-nen-background-2-9-n16-removebg-preview.png"

def load_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

bg_base64 = load_image_as_base64(BG_PATH)

# ======================
# CSS (BLUR + OVERLAY + CHỮ TRẮNG)
# ======================

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
    backdrop-filter: blur(22px);
    background: rgba(0, 0, 0, 0.60);
    z-index: 0;
}}

.block-container {{
    position: relative;
    z-index: 10;
    color: #ffffff !important;
    text-shadow: 0px 0px 8px rgba(0,0,0,0.9);
}}

h1, h2, h3, h4, h5, h6, p, label, span {{
    color: #ffffff !important;
    text-shadow: 0px 0px 8px rgba(0,0,0,0.7);
}}

.stButton>button {{
    background: linear-gradient(90deg, #ffee66, #ff9933);
    color: black;
    border: none;
    padding: 10px 24px;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
}}

.stButton>button:hover {{
    opacity: 0.9;
}}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)

# ======================
# TITLE
# ======================
st.title("🎯 Công Cụ Chia Đội Thể Thao Ngẫu Nhiên")
st.write("Hệ thống sẽ chia tự động thành 4 đội cân bằng.")

# ======================
# UPLOAD FILES
# ======================
st.subheader("📤 Upload Danh Sách Chính (Tất Cả Người Chơi)")
file_main = st.file_uploader("Chọn file Excel", type=["xlsx"])

st.subheader("📤 Upload Danh Sách Hạt Giống (Biết Chơi)")
file_seeds = st.file_uploader("Chọn file Excel", type=["xlsx"])

# ======================
# FIXED TEAM LEADERS
# ======================
st.subheader("🌈 Đội Trưởng Cố Định")

leaders = {
    "Xanh Dương": st.text_input("Đội trưởng Xanh Dương", "Leader Blue"),
    "Đỏ": st.text_input("Đội trưởng Đỏ", "Leader Red"),
    "Vàng": st.text_input("Đội trưởng Vàng", "Leader Yellow"),
    "Xanh Lá": st.text_input("Đội trưởng Xanh Lá", "Leader Green"),
}

colors = list(leaders.keys())

# ======================
# PROCESSING
# ======================
if st.button("🎲 Bắt đầu chia đội"):

    if file_main is None:
        st.error("⚠️ Bạn chưa upload danh sách chính!")
    else:
        df_main = pd.read_excel(file_main)
        main_list = df_main.iloc[:, 1].dropna().astype(str).tolist()

        seeds_list = []
        if file_seeds:
            df_seeds = pd.read_excel(file_seeds)
            seeds_list = df_seeds.iloc[:, 1].dropna().astype(str).tolist()

        # Remove duplicates
        main_list_clean = [p for p in main_list if p not in seeds_list]

        random.shuffle(main_list_clean)
        random.shuffle(seeds_list)

        teams = {c: [leaders[c]] for c in colors}

        # Assign main list
        for i, p in enumerate(main_list_clean):
            teams[colors[i % 4]].append(p)

        # Assign seeds list
        for i, s in enumerate(seeds_list):
            teams[colors[i % 4]].append(s)

        # Build output table
        max_len = max(len(team) for team in teams.values())
        df_output = pd.DataFrame({
            team: members + [""] * (max_len - len(members))
            for team, members in teams.items()
        })

        st.success("🎉 Chia đội thành công!")
        st.dataframe(df_output)

        # Excel export
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_output.to_excel(writer, index=False)

        st.download_button(
            "📥 Tải file Excel",
            buffer.getvalue(),
            "ket_qua_chia_doi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
