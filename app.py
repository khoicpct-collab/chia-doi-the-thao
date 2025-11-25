import streamlit as st
import pandas as pd
import random
from io import BytesIO

# --- UI / Background CSS ---
st.set_page_config(page_title="Chia Đội Ngẫu Nhiên", page_icon="🏖️", layout="wide")

page_bg = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url('https://st.depositphotos.com/1020288/3162/i/950/depositphotos_31620697-stock-photo-sexy-backs-of-five-beautiful.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
/* Tạo khung trắng mờ để nội dung dễ đọc */
.block-container {{
    background: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 15px;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Nội dung chính ---
st.title("🏖️ Bãi Biển Bóng Chuyền – Công Cụ Chia 4 Đội Ngẫu Nhiên 🏐")
st.write("Giao diện bãi biển, upload file danh sách để hệ thống tự chia đội, cân bằng giữa các đội.")

# --- Upload File ---
st.subheader("📤 Upload File Danh Sách Chính")
file_main = st.file_uploader("Chọn file Excel chứa danh sách tất cả người chơi", type=["xlsx"])

st.subheader("📤 Upload File Danh Sách Hạt Giống")
file_seeds = st.file_uploader("Chọn file Excel chứa danh sách hạt giống (biết chơi)", type=["xlsx"])

# --- Đội Trưởng ---
st.subheader("🌈 Đội Trưởng Cố Định")
leaders = {
    "Xanh Dương": st.text_input("Đội trưởng Xanh Dương", "Leader Blue"),
    "Đỏ": st.text_input("Đội trưởng Đỏ", "Leader Red"),
    "Vàng": st.text_input("Đội trưởng Vàng", "Leader Yellow"),
    "Xanh Lá": st.text_input("Đội trưởng Xanh Lá", "Leader Green"),
}

# --- Xử lý chia đội ---
if st.button("🎲 Bắt đầu chia đội"):
    if file_main is None:
        st.error("Vui lòng upload danh sách chính.")
    else:
        df_main = pd.read_excel(file_main)
        main_list = df_main.iloc[:, 1].dropna().astype(str).tolist()

        seeds_list = []
        if file_seeds:
            df_seeds = pd.read_excel(file_seeds)
            seeds_list = df_seeds.iloc[:, 1].dropna().astype(str).tolist()

        main_list_clean = [p for p in main_list if p not in seeds_list]

        random.shuffle(main_list_clean)
        random.shuffle(seeds_list)

        colors = list(leaders.keys())
        teams = {c: [leaders[c]] for c in colors}

        for i, p in enumerate(main_list_clean):
            teams[colors[i % 4]].append(p)

        for i, s in enumerate(seeds_list):
            teams[colors[i % 4]].append(s)

        max_len = max(len(team) for team in teams.values())
        df_output = pd.DataFrame({team: members + [""] * (max_len - len(members))
                                  for team, members in teams.items()})

        st.success("🎉 Chia đội thành công!")
        st.dataframe(df_output)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_output.to_excel(writer, index=False)
        st.download_button(
            label="📥 Tải file Excel kết quả",
            data=output.getvalue(),
            file_name="ket_qua_chia_doi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
