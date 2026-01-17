import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import os

# 1. 데이터 로드 (파일 경로를 직접 지정하세요)
# 예: 같은 폴더에 파일이 있다면 '파일명.csv'만 적으면 됩니다.
input_file = 'ev_processed.csv'  # <-- 실제 파일명으로 수정하세요!

if not os.path.exists(input_file):
    print(f"❌ 에러: '{input_file}' 파일을 찾을 수 없습니다. 경로를 확인하세요.")
else:
    df = pd.read_csv(input_file, encoding='utf-8-sig', dtype=object)

    # 2. 데이터 필터링: 설치 불가능 지역 제거
    df['exclude'] = pd.to_numeric(df['exclude'], errors='coerce').fillna(0)
    df_valid = df[df['exclude'] != 1].copy().reset_index(drop=True)

    # 3. 분석 피처 설정 및 수치형 변환
    features = ['s_population', 's_poi', 's_poi_spatial', 's_capacity_lack', 's_pop_per_charger']
    for col in features:
        df_valid[col] = pd.to_numeric(df_valid[col], errors='coerce').fillna(0)

    # 4. K-Means 클러스터링
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)
    raw_clusters = kmeans.fit_predict(df_valid[features])

    # --- [군집 번호 재부여 로직] ---
    cluster_means_raw = df_valid.groupby(raw_clusters)[features].mean()
    c_poi = cluster_means_raw['s_poi'].idxmax()
    c_unnecessary = cluster_means_raw.sum(axis=1).idxmin()
    c_pop = [i for i in range(3) if i not in [c_poi, c_unnecessary]][0]

    mapping = {c_poi: 0, c_pop: 1, c_unnecessary: 2}
    df_valid['cluster'] = pd.Series(raw_clusters).map(mapping)

    # 5. 가중합 모델링
    def run_scoring_model(data):
        data['fast_score'] = (
            (data['s_poi'] * 0.55) + (data['s_capacity_lack'] * 0.20) +
            (data['s_pop_per_charger'] * 0.20) + (data['s_population'] * 0.05)
        )
        data['slow_score'] = (
            (data['s_population'] * 0.55) + (data['s_capacity_lack'] * 0.20) +
            (data['s_pop_per_charger'] * 0.20) + (data['s_poi'] * 0.05)
        )
        return data

    df_valid = run_scoring_model(df_valid)

    # 6. 리포트 출력
    final_cluster_report = df_valid.groupby('cluster')[features].mean().sort_index()
    print("\n" + "="*75)
    print(f"📊 [분석 결과] 총 {len(df_valid)}개 격자 분석 완료")
    print("-" * 75)
    print(final_cluster_report)
    print("="*75)

    # 7. 최종 Top 3 추출
    print("\n🚀 [급속 최적 입지 TOP 3]")
    print(df_valid.nlargest(3, 'fast_score')[['grid_id', 'cluster', 'fast_score', 's_poi']])
    print("\n🏠 [완속 최적 입지 TOP 3]")
    print(df_valid.nlargest(3, 'slow_score')[['grid_id', 'cluster', 'slow_score', 's_population']])

    # 8. 파일 저장 (다운로드 함수 대신 일반 저장 사용)
    output_name = 'ev_ml_filtered_final_report.csv'
    df_valid.to_csv(output_name, index=False, encoding='utf-8-sig')
    print(f"\n✅ 저장 완료: {os.path.abspath(output_name)}")