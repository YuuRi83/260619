import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="글로벌 Top 10 주식 대시보드", layout="wide")

st.title("📈 글로벌 시가총액 Top 10 주식 대시보드")
st.markdown("최근 1년 동안의 글로벌 시가총액 상위 10개 기업의 주가 추이를 보여줍니다.")

# 2. 글로벌 시가총액 상위 10개 기업 (미국 시장 상장/ADR 기준)
TOP_10_COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'NVIDIA': 'NVDA',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Meta': 'META',
    'Berkshire Hathaway': 'BRK-B',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Broadcom': 'AVGO'
}

# 3. 데이터 로드 함수 (캐싱 적용으로 속도 향상)
@st.cache_data(ttl=3600) # 1시간 단위 캐시 갱신
def get_stock_data():
    df_list = []
    for company, ticker in TOP_10_COMPANIES.items():
        stock = yf.Ticker(ticker)
        # 최근 1년 데이터 로드
        hist = stock.history(period="1y").reset_index()
        
        if not hist.empty:
            # 시간대(Timezone) 정보 제거하여 순수 날짜만 추출
            hist['Date'] = pd.to_datetime(hist['Date']).dt.date
            hist['Company'] = company
            hist['Ticker'] = ticker
            df_list.append(hist[['Date', 'Close', 'Company', 'Ticker']])
            
    return pd.concat(df_list, ignore_index=True)

# 데이터 로딩 스피너
with st.spinner('실시간 주식 데이터를 불러오는 중입니다...'):
    df = get_stock_data()

# 4. 사이드바 UI 구성
st.sidebar.header("⚙️ 대시보드 설정")
selected_companies = st.sidebar.multiselect(
    "비교할 기업을 선택하세요",
    options=list(TOP_10_COMPANIES.keys()),
    default=list(TOP_10_COMPANIES.keys()) # 기본값: 전체 선택
)

# 5. 메인 화면 데이터 시각화
if not selected_companies:
    st.warning("👈 사이드바에서 최소 한 개의 기업을 선택해주세요.")
else:
    # 선택된 기업 데이터만 필터링
    filtered_df = df[df['Company'].isin(selected_companies)].copy()

    # 가격 비교를 위한 정규화 옵션 (첫 날 기준 0%로 시작)
    normalize = st.sidebar.checkbox("수익률(%)로 보기 (1년 전 대비)", value=True)

    if normalize:
        # 각 기업별 그룹화 후, 첫 거래일 종가 대비 변화율 계산
        filtered_df['Value'] = filtered_df.groupby('Company')['Close'].transform(lambda x: (x / x.iloc[0] - 1) * 100)
        y_title = '수익률 (%)'
        hover_format = '.2f'
    else:
        filtered_df['Value'] = filtered_df['Close']
        y_title = '주가 (USD)'
        hover_format = '.2f'

    # Plotly 시각화
    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Value', 
        color='Company',
        title='최근 1년 주가 변화 추이',
        labels={'Value': y_title, 'Date': '날짜'}
    )

    # 차트 디자인 상세 설정
    fig.update_layout(
        hovermode='x unified', # 마우스 오버 시 같은 날짜의 모든 데이터 툴팁 표시
        legend_title_text='기업 목록',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis=dict(showgrid=True, gridcolor='LightGray')
    )
    
    # y축 소수점 설정
    fig.update_yaxes(tickformat=hover_format)

    # 스트림릿에 차트 렌더링
    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터표
    with st.expander("📊 상세 데이터 확인"):
        pivot_df = filtered_df.pivot(index='Date', columns='Company', values='Close')
        pivot_df = pivot_df.sort_index(ascending=False) # 최신 날짜순
        st.dataframe(pivot_df, use_container_width=True)
