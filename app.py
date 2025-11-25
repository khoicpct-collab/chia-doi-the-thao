import streamlit as st
import pandas as pd
import random
from io import BytesIO

# --- UI ---
st.set_page_config(page_title="Chia Đội Ngẫu Nhiên", page_icon="🎯", layout="centered")
st.title("🎯 Công Cụ Chia 4 Đội Thể Thao Ngẫu Nhiên")
st.write("Upload danh sách để hệ thống tự chia thành 4 đội cân bằng, bao gồm đội trưởng và hạt giống.")

# --- Upload Files ---
st.subheader("📤 Upload File Danh Sách Chính")
file_main = st.file_uploader("Chọn file Excel chứa danh sách tất cả người chơi", type=["xlsx"])

st.subheader("📤 Upload File Danh Sách Hạt Giống")
file_seeds = st.file_uploader("Chọn file Excel chứa danh sách hạt giống (biết chơi)", type=["xlsx"])

# --- Team Leaders ---
st.subheader("🌈 Đội Trưởng Cố Định")
leaders = {
    "Xanh Dương": st.text_input("Đội trưởng Xanh Dương", "Leader Blue"),
    "Đỏ": st.text_input("Đội trưởng Đỏ", "Leader Red"),
    "Vàng": st.text_input("Đội trưởng Vàng", "Leader Yellow"),
    "Xanh Lá": st.text_input("Đội trưởng Xanh Lá", "Leader Green"),
}

# --- Process ---
if st.button("🎲 Bắt đầu chia đội"):
    if file_main is None:
        st.error("Vui lòng upload danh sách chính.")
    else:
        df_main = pd.read_excel(file_main)
        main_list = df_main.iloc[:,0].dropna().tolist()

        seeds_list = []
        if file_seeds:
            df_seeds = pd.read_excel(file_seeds)
            seeds_list = df_seeds.iloc[:,0].dropna().tolist()

        # Remove seeds from main list if duplicated
        main_list_clean = [p for p in main_list if p not in seeds_list]

        # Random shuffle
        random.shuffle(main_list_clean)
        random.shuffle(seeds_list)

        # Prepare 4 teams
        colors = list(leaders.keys())
        teams = {c: [leaders[c]] for c in colors}

        # Round-robin assign main list
        for i, p in enumerate(main_list_clean):
            teams[colors[i % 4]].append(p)

        # Round-robin assign seeds
        for i, s in enumerate(seeds_list):
            teams[colors[i % 4]].append(s)

        # Convert to DataFrame
        max_len = max(len(team) for team in teams.values())
        df_output = pd.DataFrame({team: members + [""]*(max_len-len(members)) for team, members in teams.items()})

        st.success("🎉 Chia đội thành công!")
        st.dataframe(df_output)

        # Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_output.to_excel(writer, index=False)
        st.download_button(
            label="📥 Tải file Excel kết quả",
            data=output.getvalue(),
            file_name="ket_qua_chia_doi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
