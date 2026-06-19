import streamlit as st

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="픽셀 아트 메이커 🎨", page_icon="👾", layout="centered")

# --- 2. 색상 팔레트 정의 (이모지 -> 헥스 색상 코드) ---
COLOR_MAP = {
    "⬜": "#FFFFFF", # 바탕 (흰색)
    "⬛": "#000000",
    "🟥": "#FF4B4B",
    "🟧": "#FFA500",
    "🟨": "#FFD700",
    "🟩": "#00C853",
    "🟦": "#2962FF",
    "🟪": "#AA00FF",
    "🟫": "#795548"
}
emojis = list(COLOR_MAP.keys())

# --- 3. 그리드 상태 초기화 (10x10) ---
if 'grid' not in st.session_state:
    # 각 셀을 빈 칸(하얀색 이모지)으로 채웁니다.
    st.session_state.grid = [{str(i): "⬜" for i in range(10)} for _ in range(10)]

st.markdown("<h1 style='text-align: center; color: #2962FF;'>🎨 나만의 픽셀 아트 메이커</h1>", unsafe_allow_html=True)
st.write("아래 표의 칸을 더블 클릭하고 원하는 색깔의 이모지를 선택해 그림을 그려보세요!")

# --- 4. 드롭다운 컬럼 설정 (이모지만 입력되도록 제한) ---
column_config = {
    str(i): st.column_config.SelectboxColumn(
        str(i),
        options=emojis,
        required=True
    ) for i in range(10)
}

# Streamlit 내장 데이터 에디터 렌더링
edited_grid = st.data_editor(
    st.session_state.grid,
    column_config=column_config,
    hide_index=True,
    use_container_width=True
)

# --- 5. 이미지를 코드로 변환 (SVG 생성) ---
svg_width = 400
svg_height = 400
cell_size = 40

svg_lines = [f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">']

for row_idx, row_dict in enumerate(edited_grid):
    for col_idx in range(10):
        cell_emoji = row_dict[str(col_idx)]
        color = COLOR_MAP.get(cell_emoji, "#FFFFFF")
        x = col_idx * cell_size
        y = row_idx * cell_size
        # 테두리가 얇게 들어간 사각형 그리기
        svg_lines.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" stroke="#eeeeee" stroke-width="1"/>')

svg_lines.append('</svg>')
svg_code = "\n".join(svg_lines)

# --- 6. PDF 자동 저장을 위한 HTML 래퍼 ---
# window.print()를 사용해 열자마자 인쇄(PDF 저장) 창을 띄웁니다.
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pixel Art PDF Export</title>
    <style>
        body {{ display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: white; }}
        @media print {{
            @page {{ size: auto; margin: 0mm; }}
            body {{ background-color: white; -webkit-print-color-adjust: exact; }}
        }}
    </style>
</head>
<body onload="window.print()">
    {svg_code}
</body>
</html>
"""

st.write("---")
st.subheader("🖨️ PDF로 저장하기")
st.info("💡 아래 버튼을 눌러 다운로드된 파일을 더블클릭해서 열어보세요. 브라우저에서 인쇄 창이 자동으로 뜨면 대상을 **'PDF로 저장'**으로 선택하시면 됩니다!")

# 다운로드 버튼 구현
st.download_button(
    label="📥 픽셀 아트 다운로드 (자동 PDF 변환기)",
    data=html_content,
    file_name="my_pixel_art.html",
    mime="text/html"
)
