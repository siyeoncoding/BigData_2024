import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# 1. 노인교통사고 엑셀 파일 불러오기
traffic_accidents = pd.read_excel('C:/Users/siso7/BigData_2024/exel/노인교통사고.xlsx')

# 2. '시군구'에서 서울특별시만 포함된 데이터 추출
seoul_data = traffic_accidents[traffic_accidents['시군구'].str.contains('서울특별시', na=False)]

# 3. '지점명'에서 구_동 추출
def create_gu_dong(row):
    # 지점명에서 구_동 부분을 추출 (괄호 안의 내용 제외)
    district_info = row['지점명'].split('(')[0].strip()  # 괄호 안의 부분 제거
    # '서울특별시' 제거
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



# 3. 두 파일을 '구_동' 열을 기준으로 합치기 (inner join)
merged_data = pd.merge(traffic_accidents, crosswalk_grouped, on='구_동', how='outer')
print(merged_data.describe())

'''

# 4. 서로 다른 '구_동' 이름 찾기
traffic_accidents_gudong = set(traffic_accidents['구_동'].unique())
crosswalk_grouped_gudong = set(crosswalk_grouped['구_동'].unique())

# 노인교통사고 파일에만 있는 구_동
only_in_traffic = traffic_accidents_gudong - crosswalk_grouped_gudong
print("노인교통사고 파일에만 있는 구_동:", only_in_traffic)

# crosswalk_grouped_cleaned.csv 파일에만 있는 구_동
only_in_crosswalk = crosswalk_grouped_gudong - traffic_accidents_gudong
print("횡단보도 파일에만 있는 구_동:", only_in_crosswalk)



# 노인교통사고 파일에만 있는 구_동에 해당하는 행 제거
traffic_accidents_cleaned = traffic_accidents[~traffic_accidents['구_동'].isin(only_in_traffic)]

# 결과 출력
#print("노인교통사고 파일에만 있는 구_동 행 제거 후 데이터:")
#print(traffic_accidents_cleaned.head())
'''

# 구_동별로 사고건수, 사상자수, 사망자수, 중상자수, 경상자수 합계 계산
accident_summary = merged_data.groupby('구_동')[['사고건수', '사상자수', '사망자수', '중상자수', '경상자수']].sum().reset_index()

# 결과 출력
print(accident_summary.head())

# 구_동별로 사고건수, 사상자수, 사망자수, 중상자수, 경상자수 합계 계산
accident_summary = merged_data.groupby('구_동')[['사고건수', '사상자수', '사망자수', '중상자수', '경상자수']].sum().reset_index()
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


#accident_summary_cleaned_sorted.to_excel('C:/Users/siso7/BigData_2024/exel/result.xlsx', index=False)


