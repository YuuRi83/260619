import streamlit as st
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="익명 응원 트리 🎄",
    page_icon="💌",
    layout="centered"
)

# --- 2. 초기 데이터 (세션 상태) 설정 ---
# 10개의 오너먼트 메시지 저장용 딕셔너리
if 'tree_messages' not in st.session_state:
    st.session_state.tree_messages = {i: "" for i in range(1, 11)}

# 현재 선택된 오너먼트 번호
if 'selected_ornament' not in st.session_state:
    st.session_state.selected_ornament = None

# --- 3. 화려한 커스텀 CSS ---
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        color: #2E7D32;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-weight: bold;
        margin-bottom: 30px;
    }
    /* 버튼(오너먼트)을 동그랗고 크게 만드는 마법 */
    div.stButton > button {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        font-size: 35px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px dashed #ccc !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: auto;
        display: block;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.15);
        border: 2px solid #FFD700 !important;
        box-shadow: 0 0 15px #FFD700;
        background-color: #fff !important;
    }
    .trunk {
        width: 50px;
        height: 70px;
        background: linear-gradient(to right, #5D4037, #8D6E63);
        margin: 0 auto;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .message-card {
        background: linear-gradient(135deg, #FFF9C4, #FFE082);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
        animation: fadeIn 0.8s;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 메인 화면 ---
st.markdown("<p class='main-title'>🎄 우리 반 익명 응원 트리 🎄</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>하얀색 오너먼트(⚪)를 눌러 친구들에게 따뜻한 메시지를 달아주세요!</p>", unsafe_allow_html=True)

# 오너먼트 아이콘 매핑 함수 (메시지가 있으면 예쁜 아이콘, 없으면 하얀 구슬)
def get_icon(idx):
    filled_icons = ["🌟", "🍎", "🎀", "🔔", "🎁", "🔮", "💖", "🌈", "🧸", "🍀"]
    return filled_icons[idx-1] if st.session_state.tree_messages[idx] else "⚪"

st.write("")

# --- 5. 트리 모양 레이아웃 설계 (피라미드 형태) ---
# 1층 (1개)
c1_1, c1_2, c1_3 = st.columns([2, 1, 2])
with c1_2:
    if st.button(get_icon(1), key="btn1"): st.session_state.selected_ornament = 1

# 2층 (2개)
c2_1, c2_2, c2_3, c2_4, c2_5 = st.columns([1.5, 1, 0.2, 1, 1.5])
with c2_2:
    if st.button(get_icon(2), key="btn2"): st.session_state.selected_ornament = 2
with c2_4:
    if st.button(get_icon(3), key="btn3"): st.session_state.selected_ornament = 3

# 3층 (3개)
c3_1, c3_2, c3_3, c3_4, c3_5 = st.columns([1, 1, 1, 1, 1])
with c3_2:
    if st.button(get_icon(4), key="btn4"): st.session_state.selected_ornament = 4
with c3_3:
    if st.button(get_icon(5), key="btn5"): st.session_state.selected_ornament = 5
with c3_4:
    if st.button(get_icon(6), key="btn6"): st.session_state.selected_ornament = 6

# 4층 (4개)
c4_1, c4_2, c4_3, c4_4, c4_5, c4_6 = st.columns([0.5, 1, 1, 1, 1, 0.5])
with c4_2:
    if st.button(get_icon(7), key="btn7"): st.session_state.selected_ornament = 7
with c4_3:
    if st.button(get_icon(8), key="btn8"): st.session_state.selected_ornament = 8
with c4_4:
    if st.button(get_icon(9), key="btn9"): st.session_state.selected_ornament = 9
with c4_5:
    if st.button(get_icon(10), key="btn10"): st.session_state.selected_ornament = 10

# 나무 기둥
st.markdown("<div class='trunk'></div>", unsafe_allow_html=True)
st.write("---")

# --- 6. 메시지 작성 및 확인 섹션 ---
if st.session_state.selected_ornament is not None:
    idx = st.session_state.selected_ornament
    
    # 이미 메시지가 있는 경우 (확인 모드)
    if st.session_state.tree_messages[idx]:
        st.markdown(f"""
        <div class='message-card'>
            <h3 style='color: #D84315; margin-bottom: 10px;'>💌 누군가 남긴 따뜻한 한마디</h3>
            <p style='font-size: 1.5rem; font-weight: bold; color: #333;'>"{st.session_state.tree_messages[idx]}"</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("닫기 ✖️"):
            st.session_state.selected_ornament = None
            st.rerun()
            
    # 메시지가 없는 경우 (작성 모드)
    else:
        st.info(f"✨ {idx}번 오너먼트는 비어있어요. 첫 번째 응원 메시지를 달아주세요!")
        
        # 텍스트 입력 폼
        with st.form(key=f"form_{idx}"):
            new_msg = st.text_input("👇 여기에 익명 메시지를 적어주세요 (최대 50자)", max_chars=50)
            submit = st.form_submit_button("나무에 예쁘게 매달기 🎀")
            
            if submit:
                if new_msg.strip() == "":
                    st.warning("메시지를 입력해야 매달 수 있어요!")
                else:
                    st.session_state.tree_messages[idx] = new_msg
                    st.session_state.selected_ornament = None # 작성 완료 후 닫기
                    st.balloons() # 축하 풍선 효과!
                    st.rerun() # 화면 새로고침하여 트리 업데이트
