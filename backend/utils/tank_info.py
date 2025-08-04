import pandas as pd

# def get_tank_info_from_csv(tank_name):
#     df = pd.read_csv('tank_concat.csv')

#     # 바뀐 컬럼명 "Name"을 기준으로 탐색
#     match = df[df['Name'] == tank_name]

#     if match.empty:
#         return None

#     # name 필드를 추가로 포함하려면 key를 맞춰주기
#     info = match.iloc[0].to_dict()
#     info['name'] = info['Name']  # 하위 템플릿에서 {{ tank.name }}을 유지하고 싶을 경우
#     return info

def get_tank_info_from_csv(class_name):
    df = pd.read_csv("tank_concat.csv")
    df.columns = [col.strip() for col in df.columns]  # 컬럼명 공백 제거
    tank_info = df[df["Name"] == class_name]
    return tank_info.to_dict(orient="records")[0] if not tank_info.empty else None
