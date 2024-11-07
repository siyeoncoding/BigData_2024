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
