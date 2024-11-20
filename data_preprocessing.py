import pandas as pd

# 엑셀 파일을 불러오기
file_path = 'C:/Users/siso7/BigDataProject/exel/서울시 교통안전시설물 횡단보도 정보_1.xlsx'

# 첫 번째 시트와 두 번째 시트를 불러오기
df1 = pd.read_excel(file_path, sheet_name='서울시 교통안전시설물 횡단보도 정보')  # 첫 번째 시트
df2 = pd.read_excel(file_path, sheet_name='Sheet1')  # 두 번째 시트

# 열 이름에 공백이 포함되어 있는 경우 처리
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# df1에 구이름과 동이름 열 추가
df1['구이름'] = None
df1['동이름'] = None

# df2의 시군구코드와 법정동코드를 문자열로 변환
df2['시군구코드'] = df2['시군구코드'].astype(str)
df2['법정동코드'] = df2['법정동코드'].astype(str)

# 결측값 처리: NaN을 0으로 대체 (필요시 적절한 값으로 수정)
df1['구코드'] = df1['구코드'].fillna(0).astype(int)
df1['동코드'] = df1['동코드'].fillna(0).astype(int)

# df1의 각 행을 순회하여 구이름과 동이름 추가
for index, row in df1.iterrows():
    # df1의 구코드와 df2의 시군구코드를 비교
    gu_code = str(row['구코드']).zfill(3)  # 3자리로 맞춤
    dong_code = str(row['동코드']).zfill(5)  # 5자리로 맞춤

    # df2의 시군구코드에서 앞 두 글자를 제거하고 3자리로 맞춤
    si_gun_gu_code = df2['시군구코드'].str[2:].str.zfill(3)

    # df2에서 구코드와 동코드가 일치하는 행 찾기
    matching_row = df2[(si_gun_gu_code == gu_code) & (df2['법정동코드'] == dong_code)]

    # 일치하는 행이 있는 경우 구이름과 동이름을 df1에 추가
    if not matching_row.empty:
        df1.at[index, '구이름'] = matching_row['구이름'].values[0]
        df1.at[index, '동이름'] = matching_row['동이름'].values[0]
    #else:
        # 디버깅을 위한 출력 추가
        #print(f"일치하지 않는 행: 구코드={gu_code}, 동코드={dong_code}")

# 강남구 청담동의 구코드와 동코드 찾기
filtered_row_2 = df1[(df1['구이름'] == '강남구') & (df1['동이름'] == '청담동')]
if not filtered_row_2.empty:
    gu_code_2 = filtered_row_2['구코드'].values[0]
    dong_code_2 = filtered_row_2['동코드'].values[0]
    print(f"강남구 청담동의 구코드: {gu_code_2}, 동코드: {dong_code_2}")
else:
    print("강남구 청담동의 행을 찾을 수 없습니다.")

# 결과 데이터프레임 출력 (선택 사항)
print(df1[['횡단보도관리번호', '구코드', '구이름', '동코드', '동이름']].head(3))

# 첫 번째 시트만 csv 파일로 저장
#df1.to_csv('/content/결과.csv', index=False)

# 열 이름에 공백이 포함되어 있는 경우 처리
#df1.columns = df1.columns.str.strip()

# 공사형태가 공백인 행을 삭제
df_cleaned = df1[df1['공사형태 (공통)'] != ' ']

# 횡단보도종류코드가 5 또는 6인 행을 제거
df_cleaned = df_cleaned[~df_cleaned['횡단보도종류코드'].isin([5, 6])]

df_cleaned = df_cleaned.dropna(subset=['상태 (공통)', '횡단보도종류코드', '동이름', '공사형태 (공통)'])
# '구이름'과 '동이름'을 합쳐서 새로운 열 '구_동' 생성
df_cleaned['구_동'] = df_cleaned['구이름'] + ' ' + df_cleaned['동이름']



total_rows = df_cleaned.shape[0]
print(f"결측치 제거 후 총 행의 개수: {total_rows}")

#print("상태 열의 고유값:", unique_status)
#print("횡단보도종류코드 열의 고유값:", unique_crosswalk_type)
#print("공사형태 열의 고유값:", unique_construction_type)
# 'cleaned_crosswalk.csv'로 저장
#df_cleaned.to_csv('/content/cleaned_crosswalk.csv', index=False)


# 1. 상태별 열을 생성하여 '구_동'별로 상태 개수 계산
df_status = df_cleaned.pivot_table(
    index='구_동',
    columns='상태 (공통)',
    aggfunc='size',
    fill_value=0
).reset_index()

# 2. 횡단보도종류코드별 열을 생성하여 '구_동'별로 횡단보도종류코드 개수 계산
df_crosswalk_type = df_cleaned.pivot_table(
    index='구_동',
    columns='횡단보도종류코드',
    aggfunc='size',
    fill_value=0
).reset_index()

# 3. 공사형태별 열을 생성하여 '구_동'별로 공사형태 개수 계산
df_construction_type = df_cleaned.pivot_table(
    index='구_동',
    columns='공사형태 (공통)',
    aggfunc='size',
    fill_value=0
).reset_index()

# 4. 다른 열들(횡단보도 개수, 횡단보도종류코드 개수, 공사형태 개수)도 구_동별로 그룹화하여 추가
df_additional = df_cleaned.groupby('구_동').agg(
    횡단보도_개수=('구_동', 'size')  # 횡단보도 개수
).reset_index()




# 5. 상태, 횡단보도종류코드, 공사형태 데이터를 모두 병합
df_final = pd.merge(df_status, df_crosswalk_type, on='구_동', how='left')
df_final = pd.merge(df_final, df_construction_type, on='구_동', how='left')
df_final = pd.merge(df_final, df_additional, on='구_동', how='left')



# 열 이름 변경
df_final.columns = [
    '구_동', '상태_양호', '상태_파손', '상태_도색', '상태_노후',
    '종류_1', '종류_2', '종류_3', '종류_4',
    '공사_1', '공사_2', '공사_3', '공사_4', '공사_5', '공사_6', '공사_8', '공사_9', '공사_10',
    '횡단보도_개수'
]

# 상태, 횡단보도종류코드, 공사형태의 고유값 출력
unique_status = df_cleaned['상태 (공통)'].unique()
unique_crosswalk_type = df_cleaned['횡단보도종류코드'].unique()
unique_construction_type = df_cleaned['공사형태 (공통)'].unique()

# 횡단보도종류코드가 5 또는 6인 행을 제거
# 남길 고유값 설정
desired_values = [1.0, 2.0, 3.0, 4.0]

# 필터링하여 새로운 데이터프레임 생성

df_cleaned = df_cleaned[~df_cleaned['횡단보도종류코드'].isin(['5.0', '6.0'])]

df_cleaned = df_cleaned[df_cleaned['공사형태 (공통)'] != ' ']


print("상태 열의 고유값:", unique_status)
print("횡단보도종류코드 열의 고유값:", unique_crosswalk_type)
print("공사형태 열의 고유값:", unique_construction_type)

print("--------------------------------------------------------")
# 결과 출력
print(df_final.head())
df_final.describe()

print("--------------------------------------------------------")
# 데이터 출력
print(df_final.head())  # 첫 5개 행 출력
print("--------------------------------------------------------")
# describe 메서드로 통계 정보 출력
df_final_description = df_final.describe(include='all').fillna(0)  # 모든 열의 통계 정보 포함
print(df_final_description)


# 결과를 CSV 파일로 저장 -> 결과 확인.
#df_final_description.to_csv('C:/Users/siso7/BigData_2024/exel/crosswalk_grouped_cleaned.csv', index=False)













