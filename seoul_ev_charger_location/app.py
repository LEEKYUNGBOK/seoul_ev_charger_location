import streamlit as st
import os

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="NE-EV Lab | 서울 동북권 분석",
    page_icon="⚡",
    layout="wide"
)

# --- 2. 통합 디자인 (상단 여백 제거 및 하얀색 텍스트) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
    
    [data-testid="stHeader"] { display: none; }
    .block-container {
        padding-top: 2rem !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117;
        color: #F8FAFC !important;
        font-family: 'Pretendard', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #0E1117;
        border-right: 1px solid #1E293B;
    }

    .ev-card {
        background-color: #1E293B;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    
    p, span, label, li, h1, h2, h3, h4, h5, h6 { color: #F8FAFC !important; }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        background: -webkit-linear-gradient(#38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* 가중치 테이블 디자인 */
    .weight-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 15px;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    .weight-table th { background-color: #334155; color: #38BDF8 !important; padding: 12px; font-weight: 600; }
    .weight-table td {
        background-color: #1E293B;
        color: #FFFFFF !important;
        padding: 12px;
        border-bottom: 1px solid #334155;
        text-align: center;
    }
    .stAlert p { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 경로 설정 ---
EXISTING_MAP = "northeast_ev_grid_map.html"
EXCLUDE_MAP  = "check_excluded_grids.html"
RESULT_MAP   = "northeast_ev_final_map.html"
FAST_TOP1_IMG = "fast_charge1.jpg"
FAST_TOP2_IMG = "fast_charge2.jpg"
SLOW_TOP1_IMG = "slow_charge1.jpg"
SLOW_TOP2_IMG = "slow_charge2.jpg"

def load_html(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# --- 4. 사이드바 ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/lightning-bolt.png", width=60)
    st.markdown("<h2 style='color:#38BDF8;'>NE-EV Lab</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("NAVIGATION", [
        "🏠 프로젝트 홈", 
        "📍 동북권 충전기 현황", 
        "🚫 산 및 강 제외 구역", 
        "🚀 최적 입지 분석 결과",
        "⚡ 급속 추천 입지 분석", 
        "🔋 완속 추천 입지 분석"
    ])

# --- 5. 페이지별 콘텐츠 ---

if page == "🏠 프로젝트 홈":
    st.markdown("<h1 class='main-title'>⚡ 서울시 동북권 전기차 충전소 분석 플랫폼</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div class='ev-card'>
            <h3 style='color:#38BDF8;'>📌 프로젝트 개요</h3>
            <p>서울시 동북권 8개구의 지리적 특성과 충전 인프라 현황을 머신러닝 모델로 분석하여 입지 적합도 점수(Scoring)를 산출합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:white;'>🔍 주요 분석 프로세스</h3>", unsafe_allow_html=True)
        s_col1, s_col2 = st.columns(2)
        s_col1.info("**01. 현황 분석**\n기존 충전소 데이터 정제")
        s_col2.info("**02. 수요 측정**\nPOI 기반 잠재 수요 도출")
        s_col1.info("**03. 입지 제약**\n설치 불가 구역 필터링")
        s_col2.info("**04. 모델링**\n유형별 가중치 스코어링")

    with col2:
        st.markdown("""
        <div class='ev-card'>
            <h4 style='color:#818CF8;'>📉 분석 데이터 규모</h4>
            <hr style='border-color:#334155;'>
            <p>✅ <b>격자 수:</b> 동북권 2,307개</p>
            <p>✅ <b>격자 규격:</b> 300m * 300m</p>
            <p>✅ <b>자치구:</b> 성동, 광진, 동대문, 중랑, 성북, 강북, 도봉, 노원</p>
        </div>
        """, unsafe_allow_html=True)

    # --- 사라졌던 가중치 표 다시 추가 ---
    st.markdown("---")
    st.markdown("<h3 style='color:white;'>📊 유형별 가중치 설정</h3>", unsafe_allow_html=True)
    
    w_col1, w_col2 = st.columns(2)
    def make_table(weights):
        rows = "".join([f"<tr><td>{v}</td><td>{w}</td><td style='text-align:left;'>{d}</td></tr>" for v, w, d in weights])
        return f"<table class='weight-table'><tr><th>변수</th><th>가중치</th><th>설계 근거</th></tr>{rows}</table>"

    with w_col1:
        st.markdown("<h5 style='color:#38BDF8;'>⚡ 1. 급속 충전소 모델</h5>", unsafe_allow_html=True)
        st.markdown(make_table([
            ("POI 밀집도", "0.3", "유동인구 및 상권 방문객 대응"),
            ("공간 가중치", "0.1", "인근 격자 시너지 효과 반영"),
            ("인구수", "0.2", "낮은 가중치로 회전율 중심 설계"),
            ("공급부족도", "0.2", "생활권 충전 편의성 증대"),
            ("충전기당 인구", "0.2", "거주 인구당 충전 접근성")
        ]), unsafe_allow_html=True)

    with w_col2:
        st.markdown("<h5 style='color:#818CF8;'>🔋 2. 완속 충전소 모델</h5>", unsafe_allow_html=True)
        st.markdown(make_table([
            ("POI 밀집도", "0.15", "기초 근린 생활 시설 반영"),
            ("공간 가중치", "0.05", "주거지 외 상권 보조 지표"),
            ("인구수", "0.4", "야간 충전 및 주거지 집중 수요"),
            ("공급부족도", "0.2", "생활권 충전 편의성 증대"),
            ("충전기당 인구", "0.2", "거주 인구당 충전 접근성")
        ]), unsafe_allow_html=True)

elif page == "⚡ 급속 추천 입지 분석":
    st.markdown("<h1 class='main-title'>⚡ 급속 충전 최적 입지 분석 (Top 1 & 2)</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='ev-card'>", unsafe_allow_html=True)
        st.subheader("🥇 급속 Top 1: 격자 1721")
        st.metric("Score", "0.92")
        if os.path.exists(FAST_TOP1_IMG): st.image(FAST_TOP1_IMG, use_container_width=True)
        st.info("**주소:** 서울시 묵동 동일로157나길 (먹골역 인근)\n\n상권과 다세대 주택 밀집 구역으로 급속 충전 회전율 극대화 가능")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='ev-card'>", unsafe_allow_html=True)
        st.subheader("🥈 급속 Top 2: 격자 0396")
        st.metric("Score", "0.92")
        if os.path.exists(FAST_TOP2_IMG): st.image(FAST_TOP2_IMG, use_container_width=True)
        st.info("**주소:** 서울시 동선동1가 동소문로20길 (성신여대역 인근)\n\n다양한 먹거리와 상권 및 교통 혼잡지역으로 급속 수요 대응 적합")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🔋 완속 추천 입지 분석":
    st.markdown("<h1 class='main-title'>🔋 완속 충전 최적 입지 분석 (Top 1 & 2)</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='ev-card'>", unsafe_allow_html=True)
        st.subheader("🥇 완속 Top 1: 격자 2151")
        st.metric("Score", "0.97")
        if os.path.exists(SLOW_TOP1_IMG): st.image(SLOW_TOP1_IMG, use_container_width=True)
        st.info("**주소:** 서울시 면목동 용마산로36길 (용마산역 인근)\n\n대규모 아파트 단지 밀집 구역으로 야간 완속 충전 수요 흡수에 최적")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='ev-card'>", unsafe_allow_html=True)
        st.subheader("🥈 완속 Top 2: 격자 0184")
        st.metric("Score", "0.95")
        if os.path.exists(SLOW_TOP2_IMG): st.image(SLOW_TOP2_IMG, use_container_width=True)
        st.info("**주소:** 서울시 월계동 마들로5길 (녹천역 인근)\n\n대규모 아파트 단지 밀집 지역으로 완속 충전기 설치 효율성 매우 높음")
        st.markdown("</div>", unsafe_allow_html=True)

# 기타 지도 페이지 로직
elif page in ["📍 동북권 충전기 현황", "🚫 산 및 강 제외 구역", "🚀 최적 입지 분석 결과"]:
    paths = {"📍 동북권 충전기 현황": EXISTING_MAP, "🚫 산 및 강 제외 구역": EXCLUDE_MAP, "🚀 최적 입지 분석 결과": RESULT_MAP}
    st.markdown(f"<h1 class='main-title'>{page}</h1>", unsafe_allow_html=True)
    html = load_html(paths[page])
    if html: st.components.v1.html(html, height=800)

st.markdown("<p style='text-align:center; color:#475569;'>© 2026 NE-EV Lab</p>", unsafe_allow_html=True)