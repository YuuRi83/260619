import streamlit as st
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="나만의 진로 클래스 찾기 🔮",
    page_icon="✨",
    layout="centered"
)

# --- 2. 커스텀 CSS (화려한 스타일링) ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.3rem;
        color: #7952B3;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .job-card {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        text-align: center;
        color: white;
        animation: fadeIn 1s ease-in-out;
    }
    .job-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .quest-box {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MBTI 데이터베이스 ---
mbti_data = {
    "ISTJ": {"icon": "👮‍♂️", "nickname": "규칙을 수호하는 철저한 관리자", "jobs": "경찰관, 회계사, 시스템 관리자, 빅데이터 분석가", "quest": "주변의 데이터를 수집하고 깔끔하게 표로 정리하는 퀘스트!"},
    "ISFJ": {"icon": "👼", "nickname": "따뜻한 마음을 가진 수호천사", "jobs": "교사, 간호사, 사회복지사, 사서", "quest": "친구의 고민을 들어주고 따뜻한 위로의 편지 쓰기 퀘스트!"},
    "INFJ": {"icon": "🧙‍♂️", "nickname": "깊은 통찰력을 지닌 선지자", "jobs": "심리 상담가, 작가, 디자이너, 예술가", "quest": "나만의 상상력을 발휘해 짧은 판타지 소설 써보기 퀘스트!"},
    "INTJ": {"icon": "♟️", "nickname": "전체를 꿰뚫어보는 전략가", "jobs": "소프트웨어 개발자, 데이터 사이언티스트, 시스템 엔지니어, 과학자", "quest": "복잡한 문제의 해결책을 나만의 '알고리즘 레시피'로 만들어보기 퀘스트!"},
    "ISTP": {"icon": "🛠️", "nickname": "호기심 많은 만능 재주꾼", "jobs": "엔지니어, 파일럿, 프로그래머, 카레이서", "quest": "망가진 물건의 원리를 파악하고 직접 고쳐보는 퀘스트!"},
    "ISFP": {"icon": "🎨", "nickname": "자유로운 영혼의 예술가", "jobs": "디자이너, 음악가, 수의사, 크리에이터", "quest": "오늘의 기분을 가장 잘 나타내는 그림 한 장 그리기 퀘스트!"},
    "INFP": {"icon": "🧚‍♂️", "nickname": "이상을 꿈꾸는 낭만주의자", "jobs": "일러스트레이터, 심리치료사, 작가, 애니메이터", "quest": "내가 만들고 싶은 이상적인 세계의 지도 그려보기 퀘스트!"},
    "INTP": {"icon": "🔬", "nickname": "끊임없이 탐구하는 논리술사", "jobs": "프로그래머, 철학자, 연구원, 해커", "quest": "평소 궁금했던 과학적 원리를 끝까지 파헤쳐보기 퀘스트!"},
    "ESTP": {"icon": "🏄‍♂️", "nickname": "스릴을 즐기는 활동가", "jobs": "사업가, 스포츠 선수, 경찰관, 소방관", "quest": "야외에서 새로운 스포츠 종목에 도전해보기 퀘스트!"},
    "ESFP": {"icon": "🥳", "nickname": "주변을 밝히는 분위기 메이커", "jobs": "연예인, 파티 플래너, 유튜버, 승무원", "quest": "친구들을 위해 깜짝 미니 파티 기획하기 퀘스트!"},
    "ENFP": {"icon": "🚀", "nickname": "열정 넘치는 스파크", "jobs": "기획자, 마케터, 방송인, 크리에이터", "quest": "아무도 생각하지 못한 기발한 발명품 아이디어 스케치하기 퀘스트!"},
    "ENTP": {"icon": "💡", "nickname": "기발한 아이디어 뱅크", "jobs": "발명가, 벤처 사업가, 정치인, 기자", "quest": "친구와 흥미로운 주제로 10분 동안 열띤 토론 해보기 퀘스트!"},
    "ESTJ": {"icon": "⚖️", "nickname": "체계를 세우는 총괄 지휘관", "jobs": "경영자, 판사, 프로젝트 매니저, 감독", "quest": "우리 반의 규칙을 더 효율적으로 개선할 방법 제안하기 퀘스트!"},
    "ESFJ": {"icon": "🤝", "nickname": "배려심 깊은 친선 대사", "jobs": "교사, 인사 담당자, 호텔 지배인, 아나운서", "quest": "도움이 필요한 친구를 찾아 하루 동안 수호천사 되어주기 퀘스트!"},
    "ENFJ": {"icon": "🗣️", "nickname": "사람들을 이끄는 카리스마 리더", "jobs": "교육가, 외교관, 강사, 영화감독", "quest": "팀 프로젝트에서 친구들의 장점을 찾아 역할 분담해주기 퀘스트!"},
    "ENTJ": {"icon": "👑", "nickname": "목표를 향해 돌진하는 지도자", "jobs": "CEO, 경영 컨설턴트, 변호사, 기획자", "quest": "내 인생의 10년 뒤 목표를 세우고 세부 계획 짜보기 퀘스트!"}
}

# --- 4. 메인 화면 UI ---
st.markdown("<p class='main-title'>✨ 나의 숨겨진 진로 클래스 찾기 ✨</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>플레이어님의 MBTI를 선택하고 새로운 퀘스트를 받아보세요!</p>", unsafe_allow_html=True)
st.write("---")

# MBTI 선택 드롭다운 (가운데 정렬을 위해 컬럼 사용)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_mbti = st.selectbox(
        "👇 당신의 MBTI를 선택해주세요!",
        options=["선택하세요"] + list(mbti_data.keys()),
        index=0
    )

st.write("")
st.write("")

# --- 5. 결과 출력 로직 ---
if selected_mbti != "선택하세요":
    # 로딩 애니메이션 (분석하는 느낌 주기)
    with st.spinner('크리스탈 구슬이 플레이어님의 잠재력을 분석하고 있습니다... 🔮'):
        time.sleep(1.5) # 1.5초 대기
    
    st.balloons() # 축하 풍선 효과!
    
    data = mbti_data[selected_mbti]
    
    # 결과 카드 렌더링
    st.markdown(f"""
    <div class="job-card">
        <div style="font-size: 4rem;">{data['icon']}</div>
        <div class="job-title">{selected_mbti} : {data['nickname']}</div>
        <p style="font-size: 1.2rem; margin-top: 10px;"><b>🌟 추천 직업 클래스:</b><br>{data['jobs']}</p>
        <div class="quest-box">
            📜 <b>첫 번째 퀘스트:</b> {data['quest']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.info("💡 **Tip:** 위 직업들은 추천일 뿐이에요! 플레이어님의 진짜 능력치는 무한하다는 걸 잊지 마세요. 🚀")
