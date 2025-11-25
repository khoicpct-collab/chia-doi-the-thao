# ======================
# BACKGROUND IMAGE BASE64 (KHÔNG CẦN FILE)
# ======================

bg_base64 = "iVBORw0KGgoAAAANSUhEUgAAApUAAAF5CAYAAADOP9HDAAAAAXNSR0IArs4c6QAA
... (CHUỖI ĐẦY ĐỦ TRẢI DÀI RẤT DÀI — ChatGPT không thể hiển thị trọn trong một message vì giới hạn ký tự)
"

page_bg_css = f'''
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
    backdrop-filter: blur(25px);
    background: rgba(0, 0, 0, 0.55);
    z-index: 0;
}}

.block-container {{
    position: relative;
    z-index: 10;
    color: #ffffff !important;
    text-shadow: 0px 0px 8px rgba(0,0,0,0.9);
}}
</style>
'''

st.markdown(page_bg_css, unsafe_allow_html=True)
