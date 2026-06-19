import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 페이지 기본 설정
st.set_page_config(page_title="나의 탄생일 기온 컬러 바운스", page_icon="🎨", layout="wide")

# 데이터 로드 및 전처리 (캐싱)
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

# 데이터 로딩
with st.spinner("색상을 추출하는 중..."):
    df = load_data()

# ----------------- 앱 UI -----------------
st.title("🎨 나의 탄생일 기온 컬러 바운스")
st.markdown("""
내가 태어난 날, 세상의 온도는 어떻게 변해왔을까요? 
지구 온난화 스트라이프(Warming Stripes) 아트를 기반으로 **나만의 생일 온도 바코드**를 만들어보세요.
선 위에 마우스를 올리면 해당 연도의 기온 정보가 나타납니다!
""")

# 사이드바: 생일 입력 설정창
st.sidebar.header("나의 탄생일 입력 🎂")

# 1. 연도 선택
min_year = int(df['연도'].min())
max_year = int(df['연도'].max())
birth_year = st.sidebar.number_input("태어난 연도 (Year)", min_value=min_year, max_value=max_year, value=2000)

# 2. 월 선택
birth_month = st.sidebar.selectbox("태어난 월 (Month)", list(range(1, 13)), index=4)

# 3. 일 선택 (해당 월에 맞는 일수 동적 제공)
days_in_month = df[df['월'] == birth_month]['일'].max()
birth_day = st.sidebar.selectbox("태어난 일 (Day)", list(range(1, int(days_in_month) + 1)), index=14)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** 추운 해는 파란색으로, 더운 해는 붉은색으로 표시됩니다. 색이 갈수록 붉어지고 있다면 기후 변화의 증거일 수 있습니다!")

# 선택된 생일 데이터 필터링 (태어난 해부터 마지막 연도까지 매년 그 날짜)
birthday_df = df[(df['월'] == birth_month) & (df['일'] == birth_day) & (df['연도'] >= birth_year)].copy()
birthday_df = birthday_df.sort_values('연도')

if not birthday_df.empty:
    # --- 시각적 아트워크 (컬러 바운스) 생성 로직 ---
    st.subheader(f"✨ {birth_year}년부터 기록된 {birth_month}월 {birth_day}일의 색깔")
    
    # 색상 맵 설정 (파랑 -> 하양 -> 빨강)
    cmap = plt.get_cmap('RdBu_r') 
    
    # 전체 기간이 아닌 '해당 날짜의 역대 최고/최저 기온'을 기준으로 색상 정규화 (대비 극대화)
    # 데이터가 비어있지 않은 값만 사용하여 최소/최대값 구하기
    valid_temps = birthday_df['최고기온(℃)'].dropna()
    
    if not valid_temps.empty:
        vmin = valid_temps.min()
        vmax = valid_temps.max()
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        
        # HTML/CSS 기반의 인터랙티브 스트라이프 컨테이너 생성 (툴팁 스타일 추가)
        html_code = """
        <style>
            .stripe-container {
                display: flex;
                width: 100%;
                height: 250px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                margin-top: 60px; /* 툴팁이 뜰 공간 확보 */
                margin-bottom: 20px;
                background-color: #f0f2f6;
            }
            .stripe {
                flex: 1;
                height: 100%;
                transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94), filter 0.2s;
                cursor: pointer;
                border-right: 1px solid rgba(255,255,255,0.1);
                position: relative; /* 툴팁 위치의 기준점 */
            }
            .stripe:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
            .stripe:last-child { border-top-right-radius: 8px; border-bottom-right-radius: 8px; }
            
            .stripe:hover {
                transform: scaleY(1.15); /* 바운스 효과 */
                filter: brightness(1.2);
                z-index: 10;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }
            
            /* 커스텀 말풍선(툴팁) 스타일 */
            .tooltip-content {
                visibility: hidden;
                width: max-content;
                min-width: 100px;
                background-color: rgba(40, 40, 40, 0.95);
                color: #ffffff;
                text-align: center;
                border-radius: 6px;
                padding: 10px;
                position: absolute;
                z-index: 100;
                bottom: 115%; /* 스트라이프 위로 띄움 */
                left: 50%;
                transform: translateX(-50%); /* 가운데 정렬 */
                opacity: 0;
                transition: opacity 0.2s;
                font-size: 0.85em;
                line-height: 1.5;
                pointer-events: none; /* 마우스 간섭 방지 */
                box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
            }
            
            /* 툴팁 아래쪽 뾰족한 꼬리 */
            .tooltip-content::after {
                content: "";
                position: absolute;
                top: 100%;
                left: 50%;
                margin-left: -6px;
                border-width: 6px;
                border-style: solid;
                border-color: rgba(40, 40, 40, 0.95) transparent transparent transparent;
            }

            .stripe:hover .tooltip-content {
                visibility: visible;
                opacity: 1;
            }
        </style>
        <div class="stripe-container">
        """
        
        # 각 연도별로 스트라이프(div) 그리기
        for _, row in birthday_df.iterrows():
            year = int(row['연도'])
            max_t = row['최고기온(℃)']
            min_t = row['최저기온(℃)']
            avg_t = row['평균기온(℃)']
            
            if pd.isna(max_t):
                # 데이터가 없는 연도 (예: 한국전쟁 시기)
                color = "#cccccc"
                tooltip_html = f"<strong>{year}년</strong><br/>기상 데이터 유실"
            else:
                # 기온에 따른 색상 추출
                rgba = cmap(norm(max_t))
                color = mcolors.to_hex(rgba)
                
                # 결측치 처리 (최저/평균 기온이 없는 경우 대비)
                avg_str = f"{avg_t:.1f}℃" if not pd.isna(avg_t) else "-"
                min_str = f"{min_t:.1f}℃" if not pd.isna(min_t) else "-"
                
                # 툴팁에 들어갈 내용 구성
                tooltip_html = f"<strong>{year}년</strong><br/>최고: {max_t:.1f}℃<br/>평균: {avg_str}<br/>최저: {min_str}"
                
            # HTML 요소 안에 툴팁(span) 포함
            html_code += f"<div class='stripe' style='background-color: {color};'><span class='tooltip-content'>{tooltip_html}</span></div>"
            
        html_code += "</div>"
        
        # 스트림릿에 HTML 렌더링
        st.markdown(html_code, unsafe_allow_html=True)
        
        # --- 데이터 분석 요약 ---
        st.divider()
        st.subheader("📊 내 생일 기온 TMI (Too Much Information)")
        
        # 유효한 데이터만 필터링하여 통계 계산
        stats_df = birthday_df.dropna(subset=['최고기온(℃)'])
        
        if not stats_df.empty:
            hottest_row = stats_df.loc[stats_df['최고기온(℃)'].idxmax()]
            coldest_row = stats_df.loc[stats_df['최고기온(℃)'].idxmin()]
            avg_temp_all = stats_df['최고기온(℃)'].mean()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("가장 뜨거웠던 생일 🔥", f"{int(hottest_row['연도'])}년", f"{hottest_row['최고기온(℃)']}℃")
            col2.metric("가장 서늘했던 생일 ❄️", f"{int(coldest_row['연도'])}년", f"{coldest_row['최고기온(℃)']}℃")
            col3.metric("내 생일 평균 최고기온 🌡️", f"{avg_temp_all:.1f}℃")
            
            # 꺾은선 그래프로 추이 보기
            st.write("📈 **연도별 생일 기온 변화 추이**")
            chart_data = stats_df[['연도', '최고기온(℃)']].set_index('연도')
            st.line_chart(chart_data)
        
    else:
        st.warning("해당 기간에 유효한 온도 데이터가 존재하지 않습니다.")
else:
    st.error("입력하신 날짜의 데이터를 찾을 수 없습니다. (윤달 등 날짜를 확인해 주세요)")
