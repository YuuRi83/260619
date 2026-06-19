import streamlit as st
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="알고리즘 방탈출 메이커 🚪",
    page_icon="🧩",
    layout="centered"
)

# --- 2. 화려한 게임풍 커스텀 CSS ---
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 3px 3px 0px #FFD700;
    }
    .concept-box {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #7952B3;
        margin-bottom: 20px;
    }
    .game-screen {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        padding: 30px;
        border-radius: 20px;
        color: #ffffff;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    .inventory-badge {
        background-color: #FFD700;
        color: #1e1e2f;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 초기 세션 상태 설정 (게임 데이터 및 플레이 상태 저장) ---
if 'game_data' not in st.session_state:
    st.session_state.game_data = {
        'title': '👑 마법 학원의 비밀 방',
        'item_name': '🔑 황금 열쇠',
        'start_desc': '👁️ 눈을 떠보니 어두운 마법 학원의 비밀 방에 갇혔습니다. 사방이 고요합니다.',
        'search_desc': '🧹 구석에 있는 오래된 책상을 뒤져보았습니다... 오! 서랍 깊은 곳에서 반짝이는 무언가를 발견했습니다!',
        'door_desc': '🚪 거대한 철문이 앞을 가로막고 있습니다. 문에는 정교한 열쇠구멍이 보입니다.',
        'success_msg': '🎉 찰칵! 문이 스르륵 열리며 환한 빛이 쏟아집니다! 탈출에 성공했습니다!',
        'fail_msg': '🔒 문이 굳게 잠겨 움직이지 않습니다. 아무래도 방 안을 더 조사해서 문을 열 도구를 찾아야 할 것 같습니다.'
    }

# 플레이어의 실시간 상태 변수
if 'player_has_item' not in st.session_state:
    st.session_state.player_has_item = False
if 'game_log' not in st.session_state:
    st.session_state.game_log = []
if 'current_view' not in st.session_state:
    st.session_state.current_view = "기본"

# --- 4. 메인 헤더 ---
st.markdown("<p class='main-title'>🎮 ALGORITHM ESCAPE ROOM</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>나만의 논리 분기 방탈출 게임 빌더</h3>", unsafe_allow_html=True)
st.write("---")

# 탭 구성: 설계소와 플레이 화면 분리
tab_build, tab_play = st.tabs(["🛠️ 1단계: 알고리즘 설계소", "🕹️ 2단계: 방탈출 플레이"])

# --- 5. [TAB 1] 알고리즘 설계소 (Builder Mode) ---
with tab_build:
    st.markdown("""
    <div class='concept-box'>
        <h4>💡 정보 교과서 속 알고리즘 원리 파악하기</h4>
        <ul>
            <li><b>변수(Variable):</b> 인벤토리에 들어갈 '아이템 이름'이 하나의 데이터 저장 공간(변수)이 됩니다.</li>
            <li><b>조건문(Conditional):</b> 사용자가 아이템 변수를 가졌는지(True/False) 판단하여 성공과 실패의 흐름을 나눕니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📝 게임 세계관 및 데이터(변수) 설정")
    
    # 텍스트 입력을 통해 세션 상태의 데이터를 실시간 업데이트
    st.session_state.game_data['title'] = st.text_input("💎 게임 제목을 정해주세요", st.session_state.game_data['title'])
    st.session_state.game_data['item_name'] = st.text_input("📦 탈출에 필수적인 '핵심 아이템 변수' 이름", st.session_state.game_data['item_name'])
    st.session_state.game_data['start_desc'] = st.text_area("🏠 처음 방에 진입했을 때 상황 설명 (기본 상황)", st.session_state.game_data['start_desc'])
    
    st.write("---")
    st.subheader("⚡ 조건문(If-Else) 블록 조립하기")
    
    st.info("💡 아래 구문을 완성하여 게임의 승리 조건(If)과 실패 조건(Else) 알고리즘을 설계하세요.")
    
    st.markdown(f"🟢 **만약 플레이어가 `{st.session_state.game_data['item_name']}`을(를) 획득했다면 (IF):**")
    st.session_state.game_data['search_desc'] = st.text_area("🔍 '주변 조사하기' 버튼을 눌러 아이템을 찾았을 때 출력할 문장", st.session_state.game_data['search_desc'])
    st.session_state.game_data['success_msg'] = st.text_area("🔓 아이템이 있는 상태에서 '탈출하기'를 눌렀을 때의 성공 메시지", st.session_state.game_data['success_msg'])
    
    st.markdown(f"🔴 **아니라면, 아무것도 가지지 못한 상태라면 (ELSE):**")
    st.session_state.game_data['fail_msg'] = st.text_area("🔒 아이템이 없는 상태에서 '탈출하기'를 눌렀을 때의 실패/힌트 메시지", st.session_state.game_data['fail_msg'])

    st.write("")
    if st.button("✨ 설정한 알고리즘 저장 및 검증 완료!"):
        st.success("알고리즘 구조가 뼈대에 성공적으로 주입되었습니다! 2단계 탭으로 이동해 플레이해 보세요!")
        st.balloons()

# --- 6. [TAB 2] 방탈출 플레이 (Play & Debug Mode) ---
with tab_play:
    g_data = st.session_state.game_data
    
    st.subheader(f"🎬 대기실: {g_data['title']}")
    st.caption("방금 설계소에서 빌드한 알고리즘이 실시간으로 구동되는 시뮬레이터입니다.")
    
    # 리셋 버튼
    if st.button("🔄 게임 처음부터 다시 시작 (상태 초기화)"):
        st.session_state.player_has_item = False
        st.session_state.game_log = []
        st.session_state.current_view = "기본"
        st.rerun()

    # 가상의 게임 렌더링 화면
    st.markdown(f"""
    <div class='game-screen'>
        <h2 style='color: #FFD700; text-align: center; margin-top:0;'>🏰 {g_data['title']}</h2>
        <hr style='border-color: rgba(255,255,255,0.1);'>
        <p style='font-size: 1.15rem; line-height: 1.6;'>{g_data['start_desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # 플레이어 인벤토리 상태 정보 시각화 (변수 모니터링)
    st.markdown("### 🎒 플레이어 인벤토리 (실시간 변수 상태)")
    if st.session_state.player_has_item:
        st.markdown(f"<span class='inventory-badge'>{g_data['item_name']} (보유 중: True)</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='inventory-badge' style='background-color:#555; color:#aaa;'>비어 있음 (보유 중: False)</span>", unsafe_allow_html=True)
        
    st.write("---")
    st.markdown("### 🕹️ 행동 선택하기 (이벤트 입력)")
    
    # 두 개의 핵심 선택지 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 주변 철저하게 조사하기", use_container_width=True):
            with st.spinner("방 안을 샅샅이 뒤지는 중..."):
                time.sleep(0.8)
            st.session_state.player_has_item = True
            st.session_state.current_view = "조사"
            st.session_state.game_log.append(f"계산 수행: [아이템 획득] 상태가 True로 변경되었습니다.")
            
    with col2:
        if st.button("🚪 탈출용 도어락 개방 시도", use_container_width=True):
            with st.spinner("메인 도어 알고리즘 연산 중..."):
                time.sleep(0.8)
            st.session_state.current_view = "탈출시도"
            st.session_state.game_log.append("계산 수행: [If-Else] 조건문 분기 연산이 실행되었습니다.")

    # 각 행동 결과에 따른 동적 조건문 처리 화면
    if st.session_state.current_view == "조사":
        st.success(g_data['search_desc'])
        
    elif st.session_state.current_view == "탈출시도":
        # 조건문 (IF - ELSE) 분기 로직 구현 핵심 파트
        if st.session_state.player_has_item:
            st.balloons()
            st.success(g_data['success_msg'])
        else:
            st.error(g_data['fail_msg'])

    # 디버깅용 시스템 로그 출력 (학생들에게 알고리즘의 순차 처리를 시각적으로 보여줌)
    if st.session_state.game_log:
        with st.expander("🛠️ 시스템 백엔드 알고리즘 로그 확인 (디버깅)"):
            for log in st.session_state.game_log:
                st.code(f"⚙️ {log}")
