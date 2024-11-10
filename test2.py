import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import folium
from folium import Choropleth
import geopandas as gpd

# 1. 노인교통사고 엑셀 파일 불러오기
traffic_accidents = pd.read_excel('C:/Users/siso7/BigData_2024/exel/노인교통사고.xlsx')

# 2. '시군구'에서 서울특별시만 포함된 데이터 추출
seoul_data = traffic_accidents[traffic_accidents['시군구'].str.contains('서울특별시', na=False)]

# 3. '지점명'에서 구_동 추출
def create_gu_dong(row):
    district_info = row['지점명'].split('(')[0].strip()  # 괄호 안의 부분 제거
    district_info = district_info.replace('서울특별시 ', '')
    return district_info

# 4. '구_동' 열을 새로 생성
seoul_data['구_동'] = seoul_data.apply(create_gu_dong, axis=1)

# 5. 새로운 Excel 파일로 저장
#seoul_data.to_excel('C:/Users/siso7/BigData_2024/exel/test.xlsx', index=False)

# 6. 결과 확인
print(seoul_data.head())

traffic_accidents = pd.read_excel('C:/Users/siso7/BigData_2024/exel/test.xlsx')

crosswalk_grouped = pd.read_csv('C:/Users/siso7/BigData_2024/exel/crosswalk_grouped_cleaned.csv')

# 3. 두 파일을 '구_동' 열을 기준으로 합치기 (outer join)
merged_data = pd.merge(traffic_accidents, crosswalk_grouped, on='구_동', how='outer')
print(merged_data.describe())

# 구_동별로 사고건수, 사상자수, 사망자수, 중상자수, 경상자수 합계 계산
accident_summary = merged_data.groupby('구_동')[['사고건수', '사상자수', '사망자수', '중상자수', '경상자수']].sum().reset_index()

# 결과 출력
print(accident_summary.head())

# 결측치가 있는 행을 제거
accident_summary_cleaned = accident_summary.dropna()

# 10. 0인 값이 포함된 행을 제거
accident_summary_cleaned = accident_summary_cleaned[(accident_summary_cleaned[['사고건수', '사상자수', '사망자수', '중상자수', '경상자수']] > 0).all(axis=1)]

# 결과 출력
print(accident_summary_cleaned.head())

# 사고건수를 기준으로 내림차순 정렬
accident_summary_cleaned_sorted = accident_summary_cleaned.sort_values(by='사고건수', ascending=False)

print("-----------------------------------------------------------------")
# 결과 출력
print(accident_summary_cleaned_sorted)

# 12. 서울시 구별 경계 데이터를 불러오기
seoul_gu_map = gpd.read_file('C:/Users/siso7/BigData_2024/exel/seoul.geojson')  # GeoJSON 파일 경로를 수정하세요

# 13. '서울특별시'만 포함된 데이터 필터링
seoul_gu_map = seoul_gu_map[seoul_gu_map['adm_nm'].str.contains('서울특별시')]

# '서울특별시' 부분 제거 (서울특별시만 남기고 구/동 이름 매칭)
seoul_gu_map['adm_nm'] = seoul_gu_map['adm_nm'].str.replace('서울특별시 ', '')

# 14. 사고 건수 데이터와 서울시 구별 경계를 병합합니다.
merged = seoul_gu_map.set_index('adm_nm').join(accident_summary_cleaned_sorted.set_index('구_동'))

# 15. 사고 건수 시각화를 위한 Folium 지도 생성
m = folium.Map(location=[37.5642135, 127.0016985], tiles='openstreetmap', zoom_start=11.2)

# 16. 서울시 구별 사고 건수에 따른 색상 지도 추가
choropleth = Choropleth(
    geo_data=seoul_gu_map,
    data=accident_summary_cleaned_sorted,
    columns=['구_동', '사고건수'],
    key_on='feature.properties.adm_nm',  # GeoJSON에서 구 이름을 가져옴
    fill_color='YlOrRd',  # 사고 건수에 따라 색상 적용
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='사고 건수',
    bins=[0, 10, 20, 50, 100, 150, 200],  # 사고 건수에 맞는 색상 구간 조정
).add_to(m)

folium.LayerControl().add_to(m)

# 17. 지도를 HTML로 저장
m.save('C:/Users/siso7/BigData_2024/exel/seoul_accident_map.html')

# 18. 지도를 화면에 표시
m
