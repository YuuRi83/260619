import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="기후 변화 영수증 발급기", page_icon="🧾", layout="centered")

# 데이터 로드 및 전처리 (캐싱)
@st.cache_data
def load_data():
    file_name = 'ta_20260619190504.csv'
    
    # 인코딩 예외 처리
    try:
        df = pd.read_csv(file_name, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='utf-8')
    
    # 날짜 전처리
    if df['날짜'].dtype == 'object':
        df['날짜'] = df['날짜'].str.replace('\t', '', regex=False)
    
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    # 연도, 연대 파생 변수 생성
    df['연도'] = df['날짜'].dt.year
    df['연대'] = (df['연도'] // 10) * 10 # 예: 1987 -> 1980
    return df

with st.spinner("기상 관측 영수증 단말기 부팅 중..."):
    df = load_data()

# ----------------- 앱 UI -----------------
st.title("🧾 기후 변화 영수증 발급기")
st.markdown("""
과거와 비교하여 현재 우리의 날씨는 얼마나 변했을까요? 
달라진 날씨가 우리에게 청구하는 **기후 변화 청구서**를 확인해 보세요.
""")

st.divider()

# 연대 목록 추출 (데이터가 존재하는 연대만)
decades = sorted(df['연대'].unique().tolist())

# 사이드바: 비교 기간 설정
st.sidebar.header("비교 기간 설정 ⚙️")
st.sidebar.markdown("영수증을 발급할 두 기간을 선택하세요.")

# 기본값 설정 (1980년대 vs 2020년대)
default_base_idx = decades.index(1980) if 1980 in decades else 0
default_target_idx = decades.index(2020) if 2020 in decades else len(decades) - 1

base_decade = st.sidebar.selectbox("과거 (기준 연대)", decades, index=default_base_idx)
target_decade = st.sidebar.selectbox("현재 (비교 대상 연대)", decades, index=default_target_idx)

# 연대별 평균 통계 계산 함수 (1년 기준 평균 발생 일수)
def get_decade_stats(decade):
    d_df = df[df['연대'] == decade]
    years_count = d_df['연도'].nunique()
    if years_count == 0: 
        return 0, 0, 0
    
    # 폭염 (최고기온 33도 이상), 열대야 (최저기온 25도 이상), 한파 (최저기온 -12도 이하)
    heatwaves = len(d_df[d_df['최고기온(℃)'] >= 33]) / years_count
    tropical_nights = len(d_df[d_df['최저기온(℃)'] >= 25]) / years_count
    coldwaves = len(d_df[d_df['최저기온(℃)'] <= -12]) / years_count
    
    return heatwaves, tropical_nights, coldwaves

# 발급 버튼
if st.button("영수증 발급하기 🖨️", type="primary", use_container_width=True):
    
    # 통계 계산
    base_hw, base_tn, base_cw = get_decade_stats(base_decade)
    target_hw, target_tn, target_cw = get_decade_stats(target_decade)
    
    diff_hw = target_hw - base_hw
    diff_tn = target_tn - base_tn
    diff_cw = target_cw - base_cw
    
    # 결제 비용(메시지) 매핑 로직
    cost_hw = "에어컨 누진세 폭탄 💣" if diff_hw > 0 else "선풍기로 버틸만함 🍃"
    cost_tn = "불면증 및 만성피로 🥱" if diff_tn > 0 else "숙면 가능 💤"
    cost_cw = "겨울옷 판매량 감소 🧥" if diff_cw < 0 else "보일러 연료비 증가 ♨️"
    
    # 기후 변화 종합 평가
    if diff_hw > 2 or diff_tn > 2:
        total_evaluation = "지구 온난화 심각 단계 🚨"
    elif diff_hw > 0:
        total_evaluation = "기후 변화 진행 중 ⚠️"
    else:
        total_evaluation = "안정적인 기후 유지 🌿"

    # HTML/CSS 기반의 영수증 UI 디자인
    receipt_html = f"""
    <style>
        .receipt-container {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }}
        .receipt {{
            background-color: #fcfcfc;
            width: 350px;
            padding: 30px 20px;
            box-shadow: 0px 8px 15px rgba(0,0,0,0.15);
            font-family: 'Courier New', Courier, monospace;
            color: #222;
            border-top: 6px solid #e0e0e0;
            border-bottom: 2px dashed #ccc;
        }}
        .r-title {{
            text-align: center;
            font-size: 1.4em;
            font-weight: 900;
            margin-bottom: 5px;
        }}
        .r-subtitle {{
            text-align: center;
            font-size: 0.9em;
            color: #555;
            margin-bottom: 15px;
        }}
        .r-divider {{
            border-top: 1px dashed #555;
            margin: 15px 0;
        }}
        .r-info {{
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        .r-item {{
            margin-bottom: 10px;
        }}
        .r-item-name {{
            font-weight: bold;
            font-size: 1.05em;
        }}
        .r-item-detail {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            margin-top: 3px;
        }}
        .r-diff.plus {{ color: #d32f2f; font-weight: bold; }}
        .r-diff.minus {{ color: #1976d2; font-weight: bold; }}
        .r-cost {{
            text-align: right;
            font-size: 0.85em;
            color: #666;
            margin-top: 2px;
        }}
        .r-total {{
            display: flex;
            justify-content: space-between;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
        }}
        .r-footer {{
            text-align: center;
            font-size: 0.8em;
            margin-top: 20px;
            color: #777;
        }}
    </style>

    <div class="receipt-container">
        <div class="receipt">
            <div class="r-title">기후 변화 영수증</div>
            <div class="r-subtitle">CLIMATE CHANGE RECEIPT</div>
            
            <div class="r-info">가맹점: 지구 (Earth)</div>
            <div class="r-info">고객명: 대한민국 서울 시민</div>
            <div class="r-info">비교대상: {base_decade}년대 VS {target_decade}년대</div>
            <div class="r-info">발급일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            
            <div class="r-divider"></div>
            
            <div class="r-item">
                <div class="r-item-name">🔥 연평균 폭염일수 (33℃↑)</div>
                <div class="r-item-detail">
                    <span>{base_hw:.1f}일 -> {target_hw:.1f}일</span>
                    <span class="r-diff {'plus' if diff_hw > 0 else 'minus'}">{'+' if diff_hw > 0 else ''}{diff_hw:.1f}일</span>
                </div>
                <div class="r-cost">청구항목: {cost_hw}</div>
            </div>
            
            <div class="r-item">
                <div class="r-item-name">🥵 연평균 열대야일수 (25℃↑)</div>
                <div class="r-item-detail">
                    <span>{base_tn:.1f}일 -> {target_tn:.1f}일</span>
                    <span class="r-diff {'plus' if diff_tn > 0 else 'minus'}">{'+' if diff_tn > 0 else ''}{diff_tn:.1f}일</span>
                </div>
                <div class="r-cost">청구항목: {cost_tn}</div>
            </div>
            
            <div class="r-item">
                <div class="r-item-name">🥶 연평균 한파일수 (-12℃↓)</div>
                <div class="r-item-detail">
                    <span>{base_cw:.1f}일 -> {target_cw:.1f}일</span>
                    <span class="r-diff {'plus' if diff_cw > 0 else 'minus'}">{'+' if diff_cw > 0 else ''}{diff_cw:.1f}일</span>
                </div>
                <div class="r-cost">청구항목: {cost_cw}</div>
            </div>
            
            <div class="r-divider"></div>
            
            <div class="r-total">
                <span>합계 상태</span>
                <span>{total_evaluation}</span>
            </div>
            
            <div class="r-divider"></div>
            
            <div class="r-footer">
                우리가 배출한 탄소, <br>
                결국 우리에게 비용으로 돌아옵니다.<br>
                - 자연 보호 서명 운동 -
            </div>
        </div>
    </div>
    """
    
    # 렌더링
    st.markdown(receipt_html, unsafe_allow_html=True)
    
    # 추가 통계: 기준점 및 변화 설명
    with st.expander("📊 데이터 자세히 보기"):
        st.write(f"**{base_decade}년대 대비 {target_decade}년대의 날씨 변화 요약:**")
        st.write(f"- 1년 중 최고기온이 33도를 넘는 폭염일이 평균 **{abs(diff_hw):.1f}일** {'증가' if diff_hw > 0 else '감소'}했습니다.")
        st.write(f"- 밤 최저기온이 25도 아래로 떨어지지 않는 열대야가 평균 **{abs(diff_tn):.1f}일** {'증가' if diff_tn > 0 else '감소'}했습니다.")
        st.write(f"- 최저기온이 영하 12도 이하로 떨어지는 매서운 한파 일수가 평균 **{abs(diff_cw):.1f}일** {'증가' if diff_cw > 0 else '감소'}했습니다.")
        st.info("이 영수증은 기상청에서 제공한 과거 기온 데이터를 바탕으로 1년 평균 발생 일수를 계산하여 작성되었습니다.")
