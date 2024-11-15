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


