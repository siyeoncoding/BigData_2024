import folium
import pandas as pd
import numpy as np  # numpy 임포트 추가
# 사고 데이터 불러오기
final_result = pd.read_excel('C:/Users/siso7/BigData_2024/exel/final_result.xlsx')  # 경로에 맞게 수정

# 1. 서울 지도 만들기
smap = folium.Map(location=[37.4101597, 126.6783087], zoom_start=12)

# 2. 사고 데이터 위치에 마커 추가
for name, lat, lng, accident_count in zip(final_result['구_동'], final_result['lat'], final_result['lng'], final_result['사고건수']):
    if pd.notna(lat) and pd.notna(lng):  # 위도와 경도가 NaN이 아닐 경우
        # 사고 건수에 따라 색상과 크기 조정
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

# 3. 결과 지도 저장
smap.save('C:/Users/siso7/BigData_2024/exel/1111111.html')
