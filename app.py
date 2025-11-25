bg_url = "https://st.depositphotos.com/1020288/3162/i/950/depositphotos_31620697-stock-photo-sexy-backs-of-five-beautiful.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('{bg_url}');
        background-size: cover;
        background-position: center;
    }}

    /* Overlay làm mờ */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.55); /* chỉnh độ mờ tại đây */
        backdrop-filter: blur(5px); /* hiệu ứng mờ */
        z-index: -1;
    }}

    /* Khối nội dung */
    .main-block {{
        background: rgba(255, 255, 255, 0.85);
        padding: 25px;
        border-radius: 15px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
