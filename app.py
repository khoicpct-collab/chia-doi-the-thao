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
    background: rgba(0, 0, 0, 0.55); /* tăng độ tối để chữ rõ hơn */
    z-index: 0;
}}

.block-container {{
    position: relative;
    z-index: 5;
}}

.stButton>button {{
    background: linear-gradient(90deg, #ffdd55, #ff8844);
    border: none;
    color: black;
    font-weight: 700;
    padding: 10px 26px;
    border-radius: 10px;
    cursor: pointer;
}}

.stButton>button:hover {{
    opacity: 0.85;
}}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)



# ======================
# MAIN TITLE
# ======================
st.title("🎯 Công Cụ Chia Đội Thể Thao Ngẫu Nhiên")
st.write("Upload danh sách và hệ thống sẽ chia tự động thành 4 đội cân bằng.")



# ======================
# UPLOAD FILE SECTION
# ======================
st.subheader("📤 Upload Danh Sách Chính (Tất Cả Người Chơi)")
file_main = st.file_uploader("Chọn file Excel", type=["xlsx"])

st.subheader("📤 Upload Danh Sách Hạt Giống")
file_seeds = st.file_uploader("Chọn file Excel (Hạt Giống)", type=["xlsx"])



# ======================
# LEADERS SECTION
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

        # Remove duplicate seeds
        main_list_clean = [p for p in main_list if p not in seeds_list]

        random.shuffle(main_list_clean)
        random.shuffle(seeds_list)

        teams = {c: [leaders[c]] for c in colors}

        # Assign main list
        for i, p in enumerate(main_list_clean):
            teams[colors[i % 4]].append(p)

        # Assign seeds
        for i, s in enumerate(seeds_list):
            teams[colors[i % 4]].append(s)

        max_len = max(len(team) for team in teams.values())
        df_output = pd.DataFrame({
            team: members + [""]*(max_len - len(members))
            for team, members in teams.items()
        })

        st.success("🎉 Chia đội thành công!")
        st.dataframe(df_output)

        # Excel download
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_output.to_excel(writer, index=False)

        st.download_button(
            "📥 Tải file Excel",
            buffer.getvalue(),
            "ket_qua_chia_doi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
