import streamlit as st
import pandas as pd
import random
from io import BytesIO

# ---------------- BACKGROUND + CSS ----------------
bg_url = "https://st.depositphotos.com/1020288/3162/i/950/depositphotos_31620697-stock-photo-sexy-backs-of-five-beautiful.jpg"

st.markdown(
    f"""
    <style>
    /* BACKGROUND ẢNH */
    .stApp {{
        background: url('{bg_url}');
        background-size: cover;
        background-position: center;
    }}

    /* OVERLAY MỜ ĐỂ DỄ ĐỌC CHỮ */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.55); /* độ mờ nền */
        backdrop-filter: blur(5px); /* hiệu ứng mờ */
        z-index: -1;
    }}

    /* KHỐI CHÍNH CÓ NỀN TRẮNG TRONG SUỐT */
    .main-block {{
        background: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------- PAGE SETTINGS -----------
st.set_page_config(page_title="Chia Đội Ngẫu Nhiên", page_icon="🎯", layout="centered")

# ----------- BẮT ĐẦU KHỐI NỘI DUNG -----------
st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title("🎯 Công Cụ Chia 4 Đội Thể Thao Ngẫu Nhiên")
st.write("Upload danh sách để hệ thống tự chia thành 4 đội cân bằng (bao gồm đội trưởng và hạt giống).")

# ----------- UPLOAD FILES -----------
st.subheader("📤 Upload Danh Sách Chính")
file_main = st.file_uploader("Chọn file Excel chứa danh sách tất cả người chơi", type=["xlsx"])

st.subheader("📤 Upload Danh Sách Hạt Giống (biết chơi)")
file_seeds = st.file_uploader("Chọn file Excel chứa danh sách hạt giống", type=["xlsx"])

# ----------- ĐỘI TRƯỞNG -----------
st.subheader("🌈 Đội Trưởng Cố Định")
leaders = {
    "Xanh Dương": st.text_input("Đội trưởng Xanh Dương", "Leader Blue"),
    "Đỏ": st.text_input("Đội trưởng Đỏ", "Leader Red"),
    "Vàng": st.text_input("Đội trưởng Vàng", "Leader Yellow"),
    "Xanh Lá": st.text_input("Đội trưởng Xanh Lá", "Leader Green"),
}

# ----------- XỬ LÝ CHIA ĐỘI -----------
if st.button("🎲 Quay Số & Chia Đội Ngay!"):
    if file_main is None:
        st.error("❌ Bạn chưa upload danh sách chính.")
    else:
        # Đọc danh sách chính
        df_main = pd.read_excel(file_main)
        main_list = df_main.iloc[:, 1].dropna().astype(str).tolist()

        # Đọc hạt giống
        seeds_list = []
        if file_seeds:
            df_seeds = pd.read_excel(file_seeds)
            seeds_list = df_seeds.iloc[:, 1].dropna().astype(str).tolist()

        # Loại bỏ trùng với hạt giống
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

        # Xuất Excel
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
