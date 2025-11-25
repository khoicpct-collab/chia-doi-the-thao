import streamlit as st
import pandas as pd
import random
from io import BytesIO

# ---------------- BACKGROUND ----------------
bg_url = "https://st.depositphotos.com/1020288/3162/i/950/depositphotos_31620697-stock-photo-sexy-backs-of-five-beautiful.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('{bg_url}');
        background-size: cover;
        background-position: center;
    }}

    /* Làm mờ nền phần chính */
    .main-block {{
        background: rgba(255, 255, 255, 0.82);
        padding: 25px;
        border-radius: 15px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------- UI WRAPPER -----------
st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.set_page_config(page_title="Chia Đội Ngẫu Nhiên", page_icon="🏖️", layout="centered")
st.title("🏖️🎯 Công Cụ Chia 4 Đội Ngẫu Nhiên (Beach Edition)")
st.write("Hệ thống sẽ tự động chia 4 đội cân bằng dựa trên danh sách bạn upload.")

# --- Upload Files ---
st.subheader("📤 Upload Danh Sách Chính")
file_main = st.file_uploader("Chọn file Excel chứa danh sách tất cả người chơi", type=["xlsx"])

st.subheader("📤 Upload Danh Sách Hạt Giống (biết chơi)")
file_seeds = st.file_uploader("Chọn file Excel chứa danh sách hạt giống", type=["xlsx"])

# --- Team Leaders ---
st.subheader("🌈 Đội Trưởng Cố Định")
leaders = {
    "Xanh Dương": st.text_input("Đội trưởng Xanh Dương", "Leader Blue"),
    "Đỏ": st.text_input("Đội trưởng Đỏ", "Leader Red"),
    "Vàng": st.text_input("Đội trưởng Vàng", "Leader Yellow"),
    "Xanh Lá": st.text_input("Đội trưởng Xanh Lá", "Leader Green"),
}

# --- Process split ---
if st.button("🎲 Quay Số & Chia Đội Ngay!"):
    if file_main is None:
        st.error("❌ Bạn chưa upload danh sách chính.")
    else:
        # Đọc danh sách chính
        df_main = pd.read_excel(file_main)
        main_list = df_main.iloc[:, 1].dropna().astype(str).tolist()

        # Đọc danh sách hạt giống
        seeds_list = []
        if file_seeds:
            df_seeds = pd.read_excel(file_seeds)
            seeds_list = df_seeds.iloc[:, 1].dropna().astype(str).tolist()

        # Xóa tên trùng với hạt giống
        main_list_clean = [p for p in main_list if p not in seeds_list]

        random.shuffle(main_list_clean)
        random.shuffle(seeds_list)

        # Chuẩn bị 4 đội
        colors = list(leaders.keys())
        teams = {c: [leaders[c]] for c in colors}

        # Chia danh sách chính
        for i, p in enumerate(main_list_clean):
            teams[colors[i % 4]].append(p)

        # Chia hạt giống
        for i, s in enumerate(seeds_list):
            teams[colors[i % 4]].append(s)

        # Xuất DataFrame
        max_len = max(len(team) for team in teams.values())
        df_output = pd.DataFrame({
            team: members + [""] * (max_len - len(members))
            for team, members in teams.items()
        })

        st.success("🎉 Chia đội thành công!")
        st.dataframe(df_output)

        # Tải về file Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_output.to_excel(writer, index=False)

        st.download_button(
            label="📥 Tải file Excel kết quả",
            data=output.getvalue(),
            file_name="ket_qua_chia_doi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown('</div>', unsafe_allow_html=True)
