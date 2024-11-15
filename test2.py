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

result =pd.read_excel('C:/Users/siso7/BigData_2024/exel/result.xlsx')
seoul_loc = pd.read_excel('C:/Users/siso7/BigData_2024/exel/seoul_loc.xlsx')

# seoul_loc의 'gu'와 'dong'을 합쳐서 '구_동' 열 생성
seoul_loc['구_동'] = seoul_loc['gu'] + ' ' + seoul_loc['dong']

# result의 '구_동' 열과 seoul_loc의 '구_동' 열을 기준으로 병합
final_result = pd.merge(result, seoul_loc[['구_동', 'lat', 'lng']], on='구_동', how='left')

# 병합된 데이터를 final_result.xlsx로 저장
final_result.to_excel('final_result.xlsx', index=False)


#
# # 17. final_result 확인
# print(final_result.head())
#
# # 18. 시각화: 서울 지도 만들기
# smap = folium.Map(location=[37.4101597, 126.6783087], zoom_start=12)
#
# # 19. 사고 데이터 위치에 마커 추가
# for name, lat, lng in zip(final_result['구_동'], final_result['lat'], final_result['lng']):
#     if pd.notna(lat) and pd.notna(lng):  # 위도와 경도가 NaN이 아닐 경우
#         folium.Marker([lat, lng], popup=name).add_to(smap)

# 20. 결과 지도 저장
#smap.save('C:/Users/siso7/BigData_2024/exel/seoul_accident_map.html')

#print("지도 1 시각화.")
# 10. 서울 지도 만들기

# 11. GeoJSON 파일 경로 (서울 행정구역 경계 정보)
g_geo = 'C:/Users/siso7/BigData_2024/exel/final_result.xlsx'  # 서울의 경계 GeoJSON 파일 경로로 수정
threshold_scale = [3, 32, 61, 90, 119, 148, 178]
# 12. Choropleth로 사고 건수에 따른 색상으로 구역 시각화
folium.Choropleth(
    geo_data=g_geo,  # GeoJSON 파일
    data=final_result,  # 사고 데이터
    columns=['구_동', '사고건수'],  # 구_동별 사고 건수
    key_on='feature.properties.name',  # GeoJSON 속성에 해당하는 이름
    fill_color='YlOrRd',  # 색상 설정 (Yellow to Red)
    fill_opacity=0.7,  # 투명도
    line_opacity=0.3,  # 경계선 투명도
    threshold_scale=threshold_scale,  # 사고건수에 따른 구간
).add_to(smap)

# 13. 사고 위치에 마커 추가 (사고가 많은 지역을 강조)
for name, lat, lng, accident_count in zip(final_result['구_동'], final_result['lat'], final_result['lng'], final_result['사고건수']):
    if pd.notna(lat) and pd.notna(lng):  # 위도와 경도가 NaN이 아닐 경우
        folium.CircleMarker([lat, lng],
                            radius=8,  # 반지름
                            color='red' if accident_count > 100 else 'blue',  # 사고 건수에 따라 색상
                            fill=True,
                            fill_opacity=0.7,
                            popup=f'{name}: {accident_count}건 사고'
                            ).add_to(smap)

# 14. 지도 저장
smap.save('C:/Users/siso7/BigData_2024/exel/seoul_accident_choropleth_map.html')

print("사고 다발 구역 지도 파일이 저장되었습니다.")