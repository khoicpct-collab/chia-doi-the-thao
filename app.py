import streamlit as st
import random

# ======================
# PREMIUM BEACH UI SETUP
# ======================

st.set_page_config(page_title="Chia Đội Thể Thao", layout="wide")

# Background image (local file uploaded)
background_url = "https://st.depositphotos.com/1020288/3162/i/950/depositphotos_31620697-stock-photo-sexy-backs-of-five-beautiful.jpg"

page_bg = f"""
<style>
    /* Background full page */
    .stApp {{
        background: url("{background_url}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Frosted glass overlay */
    .overlay {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.25);
        margin-bottom: 25px;
    }}

    /* Premium button gradient */
    .stButton>button {{
        background: linear-gradient(90deg, #ffb347, #ff7e5f);
        color: white;
        border: none;
        padding: 0.7em 1.5em;
        font-size: 1.1em;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(255,255,255,0.6);
    }}

    /* Input text style */
    .stTextArea textarea, .stTextInput input {{
        background: rgba(255, 255, 255, 0.6) !important;
        border-radius: 10px !important;
    }}

    /* Title shadow */
    h1, h2, h3 {{
        color: #ffffff;
        text-shadow: 0 0 8px rgba(0,0,0,0.7);
    }}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ================
# MAIN UI CONTENT
# ================

st.markdown("<div class='overlay'>", unsafe_allow_html=True)
st.title("⚡ Chia Đội Ngẫu Nhiên – Beach Edition")
st.markdown("</div>", unsafe_allow_html=True)

# Input box
st.markdown("<div class='overlay'>", unsafe_allow_html=True)
st.subheader("Nhập danh sách người chơi")
players_input = st.text_area("Mỗi tên một dòng:")
st.markdown("</div>", unsafe_allow_html=True)

# Team leaders
st.markdown("<div class='overlay'>", unsafe_allow_html=True)
st.subheader("Đội trưởng")
leader_blue = st.text_input("Đội Xanh")
leader_red = st.text_input("Đội Đỏ")
leader_yellow = st.text_input("Đội Vàng")
leader_green = st.text_input("Đội Xanh Lá")
st.markdown("</div>", unsafe_allow_html=True)

# Button
st.markdown("<div class='overlay'>", unsafe_allow_html=True)
clicked = st.button("🎲 Bấm để chia đội")
st.markdown("</div>", unsafe_allow_html=True)

# ======================
# LOGIC & RESULT DISPLAY
# ======================

if clicked:
    players = [p.strip() for p in players_input.split("\n") if p.strip()]
    leaders = {
        "Xanh": leader_blue,
        "Đỏ": leader_red,
        "Vàng": leader_yellow,
        "Xanh Lá": leader_green
    }

    player_pool = [p for p in players if p not in leaders.values()]
    random.shuffle(player_pool)

    team_names = list(leaders.keys())
    teams = {t: [leaders[t]] for t in team_names}

    i = 0
    for p in player_pool:
        teams[team_names[i]].append(p)
        i = (i + 1) % len(team_names)

    # RESULTS
    st.markdown("<div class='overlay'>", unsafe_allow_html=True)
    st.header("🏆 Kết Quả Chia Đội")

    colors = {
        "Xanh": "#007bff",
        "Đỏ": "#ff3333",
        "Vàng": "#ffcc00",
        "Xanh Lá": "#28a745"
    }

    for team_name, members in teams.items():
        st.markdown(
            f"""
            <div style="
                padding: 18px;
                margin-top: 18px;
                border-radius: 16px;
                border-left: 10px solid {colors[team_name]};
                background: rgba(255,255,255,0.55);
                backdrop-filter: blur(4px);
            ">
                <h3 style="color:{colors[team_name]}; margin-bottom:8px;">🏐 Đội {team_name}</h3>
                <ul style="color:#000; font-size:1.1em;">
                    {''.join([f"<li>{m}</li>" for m in members])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
