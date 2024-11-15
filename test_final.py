import folium
import pandas as pd
import json
import numpy as np

# 사고 데이터 불러오기
final_result = pd.read_excel('C:/Users/siso7/BigData_2024/exel/final_result.xlsx')  # 경로에 맞게 수정

# GeoJSON 형식의 서울 행정동 경계 데이터 불러오기 (인코딩을 'utf-8'로 설정)
geojson_file = 'C:/Users/siso7/BigData_2024/exel/서울_행정동.geojson'

# 서울 지도 생성 (기본 위치: 서울)
smap = folium.Map(location=[37.4101597, 126.6783087], zoom_start=12)

# GeoJSON 파일을 UTF-8로 열기
with open(geojson_file, encoding='utf-8') as f:
    geojson_data = json.load(f)

# GeoJSON의 adm_nm에서 '서울특별시 ' 부분을 제거하여 구_동과 일치시킴
for feature in geojson_data['features']:
    feature['properties']['adm_nm'] = feature['properties']['adm_nm'].replace('서울특별시 ', '')

# 사고 건수에 따른 색상 설정을 위한 threshold_scale 설정
threshold_scale = [0, 20, 50, 100, 150, 200, 250]

# Choropleth 지도 생성 (사고 건수에 따른 색상 변경)
folium.Choropleth(
    geo_data=geojson_data,  # 서울 행정동 경계 GeoJSON 파일
    data=final_result,  # 사고 데이터 (사고건수)
    columns=['구_동', '사고건수'],  # 구_동별 사고 건수
    key_on='feature.properties.adm_nm',  # GeoJSON 속성에 해당하는 '구_동' 이름
    fill_color='YlOrRd',  # 색상 설정 (Yellow to Red)
    fill_opacity=0.7,  # 투명도
    line_opacity=0.3,  # 경계선 투명도
    threshold_scale=threshold_scale,  # 사고건수에 따른 구간
    legend_name="사고 건수"
).add_to(smap)

# 사고 위치에 마커 추가 (사고가 많은 지역을 강조)
for name, lat, lng, accident_count in zip(final_result['구_동'], final_result['lat'], final_result['lng'], final_result['사고건수']):
    if pd.notna(lat) and pd.notna(lng):  # 위도와 경도가 NaN이 아닐 경우
        # 사고 건수에 따라 마커 색상과 크기 조정
        color = 'red' if accident_count > 100 else 'orange' if accident_count > 50 else 'green'  # 사고 건수에 따른 색상
        radius = np.sqrt(accident_count) * 2  # 사고 건수에 비례하여 마커 크기 설정 (radius)

        # 마커 추가
        folium.CircleMarker(
            location=[lat, lng],
            radius=radius,  # 마커 크기
            color=color,  # 마커 색상
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"{name}: {accident_count}건"  # 팝업에 사고 건수 추가
        ).add_to(smap)

# 결과 지도 저장
smap.save('C:/Users/siso7/BigData_2024/exel/서울_사고_경계선_지도.html')
