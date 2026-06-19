import streamlit as st

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="마법의 익명 트리 🎄", page_icon="✨", layout="centered")

# --- 2. 초기 데이터 (세션 상태) 설정 ---
if 'tree_messages' not in st.session_state:
    st.session_state.tree_messages = {i: "" for i in range(1, 11)}

# --- 3. 마법 같은 애니메이션 CSS ---
st.markdown("""
<style>
    /* 따뜻하고 신비로운 밤하늘 배경 */
    .tree-wrapper {
        background: linear-gradient(180deg, #0B1D3A 0%, #172A45 60%, #1E3A5F 100%);
        padding: 40px 0 60px 0;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden; /* 눈송이가 영역 밖으로 나가지 않게 */
    }
    .tree-title {
        text-align: center;
        color: #FFF3C7;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 20px;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(255,243,199,0.8);
        position: relative;
        z-index: 5;
    }
    
    /* ❄️ 끊임없이 내리는 눈 애니메이션 */
    @keyframes snowFall {
        0% { transform: translateY(-100px) translateX(0px); opacity: 1; }
        100% { transform: translateY(500px) translateX(30px); opacity: 0; }
    }
    .snow {
        position: absolute;
        top: -20px;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
        user-select: none;
        animation: snowFall linear infinite;
        z-index: 1;
    }
    /* 눈송이마다 떨어지는 속도와 위치를 다르게 설정 */
    .snow:nth-child(1) { left: 10%; animation-duration: 4s; animation-delay: 0s; }
    .snow:nth-child(2) { left: 25%; animation-duration: 5s; animation-delay: 1s; font-size: 0.9rem; }
    .snow:nth-child(3) { left: 40%; animation-duration: 3.5s; animation-delay: 2s; }
    .snow:nth-child(4) { left: 60%; animation-duration: 6s; animation-delay: 0.5s; font-size: 1.5rem; }
    .snow:nth-child(5) { left: 75%; animation-duration: 4.5s; animation-delay: 1.5s; }
    .snow:nth-child(6) { left: 90%; animation-duration: 5.5s; animation-delay: 0.2s; font-size: 0.8rem; }

    /* 트리 영역을 고정하여 오너먼트가 자연스럽게 배치되도록 함 */
    .tree-box {
        position: relative;
        width: 320px;
        height: 420px;
        margin: 0 auto;
        z-index: 5;
    }

    /* ✨ 트리의 은은한 반짝임 조명 효과 */
    @keyframes treeGlow {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(76, 175, 80, 0.3)); }
        50% { filter: drop-shadow(0 0 25px rgba(100, 255, 100, 0.6)); }
    }

    /* CSS로 그린 자연스러운 나무 잎사귀 */
    .tree-layer {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 0; height: 0;
        animation: treeGlow 4s infinite alternate;
    }
    .layer1 { bottom: 40px; border-left: 150px solid transparent; border-right: 150px solid transparent; border-bottom: 220px solid #1B5E20; }
    .layer2 { bottom: 140px; border-left: 120px solid transparent; border-right: 120px solid transparent; border-bottom: 180px solid #2E7D32; }
    .layer3 { bottom: 230px; border-left: 90px solid transparent; border-right: 90px solid transparent; border-bottom: 140px solid #4CAF50; }
    
    /* 나무 기둥 */
    .trunk {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 45px;
        height: 50px;
        background: linear-gradient(to right, #4E342E, #3E2723);
        border-radius: 4px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    /* 🌟 오너먼트의 반짝임 & 살랑거리는 애니메이션 */
    @keyframes sway {
        0%, 100% { transform: rotate(-10deg); filter: brightness(1); }
        50% { transform: rotate(10deg); filter: brightness(1.3) drop-shadow(0 0 10px rgba(255,215,0,0.8)); }
    }
    .ornament {
        position: absolute;
        font-size: 35px;
        cursor: pointer;
        animation: sway 3s infinite ease-in-out;
        transform-origin: top center;
        transition: transform 0.2s;
        z-index: 10;
    }
    /* 각 오너먼트가 제각각 움직이도록 딜레이 추가 */
    .ornament:nth-child(even) { animation-duration: 3.5s; animation-direction: reverse; }
    .ornament:nth-child(3n) { animation-duration: 4s; }

    .ornament:hover {
        z-index: 20;
        transform: scale(1.3) !important;
        filter: drop-shadow(0 0 20px #FFD700);
    }
    
    /* 호버 시 나타나는 예쁜 말풍선 툴팁 */
    .message-tooltip {
        visibility: hidden;
        width: 220px;
        background-color: rgba(255, 255, 255, 0.95);
        color: #2c3e50;
        text-align: center;
        border-radius: 15px;
        padding: 15px;
        position: absolute;
        bottom: 130%;
        left: 50%;
        margin-left: -110px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        opacity: 0;
        transition: opacity 0.3s, bottom 0.3s;
        font-size: 0.95rem;
        font-weight: 800;
        pointer-events: none;
    }
    .message-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: rgba(255, 255, 255, 0.95) transparent transparent transparent;
    }
    .ornament:hover .message-tooltip {
        visibility: visible;
        opacity: 1;
        bottom: 110%;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 오너먼트 자연스러운 배치 좌표 ---
ornament_positions = {
    1: {"bottom": "340px", "left": "calc(50% - 15px)"},  
    2: {"bottom": "280px", "left": "calc(50% - 60px)"},
    3: {"bottom": "260px", "left": "calc(50% + 20px)"},
    4: {"bottom": "190px", "left": "calc(50% - 90px)"},
    5: {"bottom": "210px", "left": "calc(50% - 10px)"},
    6: {"bottom": "180px", "left": "calc(50% + 50px)"},
    7: {"bottom": "110px", "left": "calc(50% - 120px)"},
    8: {"bottom": "130px", "left": "calc(50% - 40px)"},
    9: {"bottom": "90px",  "left": "calc(50% + 30px)"},
    10: {"bottom": "120px", "left": "calc(50% + 80px)"}
}

# --- 5. 트리 렌더링 로직 (눈 애니메이션 포함) ---
html_elements = []
html_elements.append("<div class='tree-wrapper'>")

# 배경에 내리는 눈송이들 추가
for _ in range(6):
    html_elements.append("<div class='snow'>❄️</div>")

html_elements.append("<div class='tree-title'>✨ 밤하늘의 익명 트리 ✨</div>")
html_elements.append("<div class='tree-box'>")
html_elements.append("<div class='tree-layer layer1'></div>")
html_elements.append("<div class='tree-layer layer2'></div>")
html_elements.append("<div class='tree-layer layer3'></div>")
html_elements.append("<div class='trunk'></div>")

# 오너먼트 생성
filled_icons = ["🌟", "🍎", "🎀", "🔔", "🎁", "🔮", "💖", "🌈", "🧸", "🍀"]

for idx in range(1, 11):
    msg = st.session_state.tree_messages[idx]
    icon = filled_icons[idx-1] if msg else "🫧" 
    tooltip_text = msg if msg else "비어있는 자리입니다.<br>아래에서 메시지를 달아주세요!"
    
    pos = ornament_positions[idx]
    ornament_html = f"""
    <div class='ornament' style='bottom: {pos["bottom"]}; left: {pos["left"]};'>
        {icon}
        <div class='message-tooltip'>{tooltip_text}</div>
    </div>
    """
    html_elements.append(ornament_html)

html_elements.append("</div></div>")
st.markdown("".join(html_elements), unsafe_allow_html=True)

# --- 6. 메시지 작성 폼 ---
st.markdown("### 💌 나무에 마음 달기")
st.write("위 나무에 마우스를 올려 메시지를 확인하고, 빈자리에 새로운 메시지를 추가해 보세요.")

empty_slots = [i for i in range(1, 11) if not st.session_state.tree_messages[i]]

if not empty_slots:
    st.success("나무에 모든 마음이 가득 찼습니다! 🎄✨")
    st.snow() # Streamlit 기본 눈 효과 추가 실행
else:
    with st.form("message_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_idx = st.selectbox("위치 선택", empty_slots, format_func=lambda x: f"{x}번 자리 🫧")
        with col2:
            new_msg = st.text_input("메시지 (최대 40자)", max_chars=40, placeholder="친구에게 전할 따뜻한 한마디...")
            
        submit = st.form_submit_button("트리에 매달기 🎀")
        
        if submit:
            if new_msg.strip():
                st.session_state.tree_messages[selected_idx] = new_msg
                st.rerun()
            else:
                st.warning("메시지를 입력해주세요!")
