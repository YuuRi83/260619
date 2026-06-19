import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="시간여행자의 날씨 일기", page_icon="🕰️", layout="centered")

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    file_name = 'ta_20260619190504.csv'
    
    try:
        df = pd.read_csv(file_name, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='utf-8')
    
    if df['날짜'].dtype == 'object':
        df['날짜'] = df['날짜'].str.replace('\t', '', regex=False)
    
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

# 일기장 타이핑 애니메이션을 위한 커스텀 함수
def render_typewriter(text):
    # 자바스크립트에 넣기 위해 줄바꿈 문자를 HTML 태그로 변경
    text_for_js = text.replace('\n', '<br>').replace("'", "\\'")
    
    # HTML + CSS + JS 코드로 애니메이션 구현
    html_code = f"""
    <div style="
        font-family: 'Gowun Dodum', sans-serif;
        font-size: 1.1rem;
        line-height: 1.8;
        padding: 25px;
        background-color: #fdfbf7;
        color: #333;
        border: 1px solid #e0d8c3;
        border-radius: 10px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
        min-height: 200px;
    ">
        <span id="diary-text"></span><span id="cursor" style="animation: blink 1s infinite;">✍️</span>
    </div>
    
    <style>
        /* 감성적인 한글 폰트 불러오기 */
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
        
        /* 커서 깜빡임 효과 */
        @keyframes blink {{
            0% {{opacity: 1;}}
            50% {{opacity: 0;}}
            100% {{opacity: 1;}}
        }}
    </style>
    
    <script>
        const text = '{text_for_js}';
        let i = 0;
        const element = document.getElementById("diary-text");
        const cursor = document.getElementById("cursor");
        
        function typeWriter() {{
            if (i < text.length) {{
                // <br> 태그 처리 (줄바꿈)
                if (text.substring(i, i+4) === '<br>') {{
                    element.innerHTML += '<br>';
                    i += 4;
                }} else {{
                    // 한 글자씩 출력
                    element.innerHTML += text.charAt(i);
                    i++;
                }}
                setTimeout(typeWriter, 40); // 숫자가 작을수록 타이핑 속도가 빠름
            }} else {{
                // 타이핑이 끝나면 연필 이모지 숨기기
                cursor.style.display = 'none';
            }}
        }}
        
        // 화면이 로드된 후 약간의 지연시간을 두고 타이핑 시작
        setTimeout(typeWriter, 500);
    </script>
    """
    # 스트림릿에 HTML 컴포넌트 렌더링
    components.html(html_code, height=300, scrolling=True)

# ----------------- 앱 UI -----------------
st.title("🕰️ 시간여행자의 날씨 일기")
st.markdown("과거의 오늘, 서울의 날씨는 어땠을까요? 날짜를 고르면 **그 시절의 일기장**이 실시간으로 쓰여집니다.")

with st.spinner("과거의 기상 기록을 펼치는 중..."):
    df = load_data()

st.sidebar.header("타임머신 설정 ⚙️")

years = df['연도'].dropna().unique().tolist()
selected_year = st.sidebar.selectbox("연도 (Year)", years, index=len(years)-1)

months = df[df['연도'] == selected_year]['월'].unique().tolist()
selected_month = st.sidebar.selectbox("월 (Month)", sorted(months))

days = df[(df['연도'] == selected_year) & (df['월'] == selected_month)]['일'].unique().tolist()
selected_day = st.sidebar.selectbox("일 (Day)", sorted(days))

selected_data = df[(df['연도'] == selected_year) & (df['월'] == selected_month) & (df['일'] == selected_day)]

if not selected_data.empty:
    row = selected_data.iloc[0]
    avg_t = row['평균기온(℃)']
    min_t = row['최저기온(℃)']
    max_t = row['최고기온(℃)']
    
    st.subheader(f"📅 {int(selected_year)}년 {int(selected_month)}월 {int(selected_day)}일의 기록")
    
    if pd.isna(avg_t) or pd.isna(min_t) or pd.isna(max_t):
        st.warning("아쉽게도 이 날은 역사적 사유로 인해 기온 데이터가 유실되었습니다.")
    else:
        diff_t = max_t - min_t
        
        # 기온 데이터 수치 출력
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("평균기온", f"{avg_t:.1f}℃")
        col2.metric("최저기온", f"{min_t:.1f}℃")
        col3.metric("최고기온", f"{max_t:.1f}℃")
        col4.metric("일교차", f"{diff_t:.1f}℃")
        
        st.divider()
        
        # 스토리 생성
        story = f"[{int(selected_year)}년의 당신에게...]\n\n"
        
        if min_t < 0:
            story += "아침에 눈을 뜨니 방 안의 물그릇이 꽁꽁 얼어붙었습니다! 문틈으로 스며드는 매서운 칼바람에 이불 밖으로 나오기 무섭네요. 가장 두꺼운 솜옷을 단단히 껴입고 나서야 합니다. 🥶"
            st.snow()
        elif min_t < 10:
            story += "아침저녁으로 제법 쌀쌀한 기운이 돕니다. 따뜻한 아랫목이나 난로가 생각나는 날씨네요. 외출 시 겉옷을 꼭 챙기세요."
        elif min_t > 25:
            story += "밤이 되어도 열기가 식지 않는 열대야가 찾아왔습니다. 부채질을 아무리 해도 잠들기 어려운 덥고 끈적한 밤이네요. 🥵"
        else:
            story += "아침저녁으로는 활동하기 무난하고 상쾌한 기온입니다."
            
        if max_t > 33:
            story += "\n\n한낮에는 태양이 찌는 듯이 내리쬡니다. 가급적 시원한 그늘이나 대청마루에서 한낮의 폭염을 피하는 것이 좋겠습니다. ☀️💦"
        elif max_t > 28:
            story += "\n\n낮에는 이마에 땀이 맺힐 정도로 꽤 더운 날씨입니다. 시원한 우물물로 등목을 하면 딱 좋을 것 같네요!"
            
        if diff_t > 15:
            story += f"\n\n🚨 주의: 오늘은 하루 사이 온도 변화(일교차)가 무려 {diff_t:.1f}도나 됩니다! 아침에는 오들오들 떨리다가도 한낮에는 땀이 뻘뻘 날 수 있으니, 감기 조심하세요."
        elif diff_t > 10:
            story += f"\n\n일교차가 {diff_t:.1f}도로 제법 큽니다. 외출하실 때 체온 조절에 신경 쓰세요."
        
        # 타이핑 애니메이션 적용하여 출력
        render_typewriter(story)

else:
    st.error("선택하신 날짜의 데이터를 찾을 수 없습니다.")
