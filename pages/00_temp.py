import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="시간여행자의 날씨 일기", page_icon="🕰️", layout="centered")

# 데이터 로드 및 전처리 (캐싱하여 속도 향상)
@st.cache_data
def load_data():
    file_name = 'ta_20260619190504.csv'
    
    # 기상청 데이터의 한글 인코딩(cp949) 및 utf-8 예외 처리
    try:
        df = pd.read_csv(file_name, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='utf-8')
    
    # 날짜 데이터 전처리 (숨겨진 탭('\t') 문자 제거 후 날짜형으로 변환)
    if df['날짜'].dtype == 'object':
        df['날짜'] = df['날짜'].str.replace('\t', '', regex=False)
    
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜']) # 날짜가 유효하지 않은 행 제거
    
    # 연, 월, 일 컬럼 분리
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

# 앱 UI 시작
st.title("🕰️ 시간여행자의 날씨 일기")
st.markdown("과거의 오늘, 서울의 날씨는 어땠을까요? 1907년부터의 데이터를 통해 **그 시절의 체감 온도**를 체험해 보세요!")

# 데이터 로딩
with st.spinner("과거의 기상 기록을 펼치는 중..."):
    df = load_data()

# 사이드바: 타임머신 설정창
st.sidebar.header("타임머신 설정 ⚙️")
st.sidebar.markdown("이동하고 싶은 시대를 선택하세요.")

# 연도, 월, 일 선택 (데이터가 존재하는 날짜만 선택 가능하도록 동적 구성)
years = df['연도'].dropna().unique().tolist()
selected_year = st.sidebar.selectbox("연도 (Year)", years, index=len(years)-1)

months = df[df['연도'] == selected_year]['월'].unique().tolist()
selected_month = st.sidebar.selectbox("월 (Month)", sorted(months))

days = df[(df['연도'] == selected_year) & (df['월'] == selected_month)]['일'].unique().tolist()
selected_day = st.sidebar.selectbox("일 (Day)", sorted(days))

# 선택된 날짜의 데이터 필터링
selected_data = df[(df['연도'] == selected_year) & (df['월'] == selected_month) & (df['일'] == selected_day)]

# 메인 화면: 결과 출력
if not selected_data.empty:
    row = selected_data.iloc[0]
    avg_t = row['평균기온(℃)']
    min_t = row['최저기온(℃)']
    max_t = row['최고기온(℃)']
    
    st.subheader(f"📅 {int(selected_year)}년 {int(selected_month)}월 {int(selected_day)}일의 서울")
    
    # 한국전쟁 등 데이터 유실 기간 처리
    if pd.isna(avg_t) or pd.isna(min_t) or pd.isna(max_t):
        st.warning("아쉽게도 이 날은 역사적 사유(전쟁 등)로 인해 기온 데이터가 유실되었습니다.")
    else:
        diff_t = max_t - min_t # 일교차 계산
        
        # 1. 수치 데이터 시각화
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("평균기온", f"{avg_t:.1f}℃")
        col2.metric("최저기온", f"{min_t:.1f}℃")
        col3.metric("최고기온", f"{max_t:.1f}℃")
        col4.metric("일교차", f"{diff_t:.1f}℃")
        
        st.divider()
        
        # 2. 체감형 스토리 생성 로직
        st.subheader("📝 오늘의 날씨 체험 일기")
        
        story = f"**[{int(selected_year)}년의 당신에게...]**\n\n"
        
        # 최저기온 기준
        if min_t < 0:
            story += "아침에 눈을 뜨니 방 안의 물그릇이 꽁꽁 얼어붙었습니다! 문틈으로 스며드는 매서운 칼바람에 이불 밖으로 나오기 무섭네요. 가장 두꺼운 솜옷을 단단히 껴입고 나서야 합니다. 🥶 "
            st.snow() # 영하일 때 눈 내리는 이펙트
        elif min_t < 10:
            story += "아침저녁으로 제법 쌀쌀한 기운이 돕니다. 따뜻한 아랫목이나 난로가 생각나는 날씨네요. 외출 시 겉옷을 꼭 챙기세요. 🧣 "
        elif min_t > 25:
            story += "밤이 되어도 열기가 식지 않는 열대야가 찾아왔습니다. 부채질을 아무리 해도 잠들기 어려운 덥고 끈적한 밤이네요. 🥵 "
        else:
            story += "아침저녁으로는 활동하기 무난하고 상쾌한 기온입니다. "
            
        # 최고기온 기준
        if max_t > 33:
            story += "\n\n한낮에는 태양이 찌는 듯이 내리쬡니다. 가급적 시원한 그늘이나 대청마루에서 한낮의 폭염을 피하는 것이 좋겠습니다. ☀️💦"
        elif max_t > 28:
            story += "\n\n낮에는 이마에 땀이 맺힐 정도로 꽤 더운 날씨입니다. 시원한 우물물로 등목을 하면 딱 좋을 것 같네요!"
            
        # 일교차 기준
        if diff_t > 15:
            story += f"\n\n🚨 **주의:** 오늘은 하루 사이 온도 변화(일교차)가 무려 **{diff_t:.1f}도**나 됩니다! 아침에는 오들오들 떨리다가도 한낮에는 땀이 뻘뻘 날 수 있으니, 입고 벗기 편한 옷을 여러 겹 겹쳐 입으세요. 🧥➡️👕"
        elif diff_t > 10:
            story += f"\n\n일교차가 **{diff_t:.1f}도**로 제법 큽니다. 감기에 걸리지 않게 몸을 따뜻하게 유지하세요."
            
        st.info(story)
        
        # 3. 간단한 막대 그래프
        st.subheader("📊 온도 한눈에 보기")
        chart_data = pd.DataFrame({
            "구분": ["최저기온", "평균기온", "최고기온"],
            "온도(℃)": [min_t, avg_t, max_t]
        })
        st.bar_chart(chart_data.set_index("구분"), use_container_width=True)

else:
    st.error("선택하신 날짜의 데이터를 찾을 수 없습니다.")
