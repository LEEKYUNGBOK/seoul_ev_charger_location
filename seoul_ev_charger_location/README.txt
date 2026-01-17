서울시 동북권 전기차(EV) 충전소 최적 입지 분석 프로젝트

> 머신러닝 기반 격자 스코어링 모델을 활용한 충전 인프라 배치 최적화

1. 프로젝트 개요
- 대상 지역: 서울시 동북권 8개 자치구 (성동, 광진, 동대문, 중랑, 성북, 강북, 도봉, 노원)
- 분석 단위: 300m x 300m 격자 (총 2,307개)
- 목적: 데이터 기반의 분석을 통해 급속 및 완속 충전소의 최적 후보지를 제안하여 인프라 효율성을 극대화함.

2. 기술 스택
- Language: Python 
- Library: `Pandas`, `GeoPandas`, `Folium`, `Scikit-learn`, `Streamlit`
- Data API: 공공데이터포털(전기차 충전소 정보), 서울 열린데이터 광장

3. 분석 프로세스
   1. 데이터 수집: 공공 API 및 CSV를 통한 충전소 현황, POI(주요시설), 인구 데이터 수집
   2. 데이터 전처리: 지리 데이터 격자 매핑 및 설치 불가능 지역(산, 하천) Exclude 처리
   3. 가중치 모델링: 유형별(급속/완속) 가중치 부여를 통한 스코어링
      - 급속: 상권 밀집도 및 공급 부족도 중심 가중치
      - 완속: 주거 인구 및 충전기당 인구 중심 가중치
   4. 결과 시각화: Streamlit 기반 인터랙티브 대시보드 구축

4. 모델링 및 결과
   src의 clustering_model을 통한 결과 확인 ev_processed.CSV를 넣어 모델 결과 확인

5.UI 결과 확인 
	app.py 실행 및 streamlit run app.py 입력  

6. 프로젝트 구조
   seoul_ev_charger_location
   ├── app.py              # Streamlit 대시보드 메인 실행 파일
   ├── src/                # 전처리 및 분석 스크립트 모음
   ├── data/               # 분석에 사용된 데이터셋
   └── northeast_ev_final_map.html  # 최종 결과 시각화 파일