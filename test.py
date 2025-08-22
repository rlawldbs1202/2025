import streamlit as st
import pandas as pd
import datetime

st.title("급식 메뉴 앱")
st.write("오늘 메뉴 확인과 좋아하는 메뉴 체크가 가능합니다.")

# ----- 급식 데이터 -----
menu_data = {
    "요일": ["월", "화", "수", "목", "금"],
    "메뉴": [
        "김밥, 우동, 사과",
        "비빔밥, 계란국, 바나나",
        "카레라이스, 오이무침, 귤",
        "라면, 김치전, 배",
        "떡볶이, 단무지, 요구르트"
    ],
    "칼로리": [550, 600, 580, 620, 500]
}

df = pd.DataFrame(menu_data)

# ----- 오늘 요일 계산 (월=0, 금=4) -----
today_index = datetime.datetime.today().weekday()
if today_index > 4:
    today_index = 0  # 주말은 월요일 메뉴 표시
today_menu = df.iloc[today_index]

st.subheader("오늘의 급식")
st.write(f"메뉴: {today_menu['메뉴']}")
st.write(f"칼로리: {today_menu['칼로리']} kcal")

# ----- 좋아하는 메뉴 체크 -----
st.subheader("좋아하는 메뉴 선택")
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# 체크박스별로 session_state 업데이트 (단순 루프)
for i, row in df.iterrows():
    key_name = f"menu_checkbox_{i}"
    if key_name not in st.session_state:
        st.session_state[key_name] = row["메뉴"] in st.session_state["favorites"]

    checked = st.checkbox(f"{row['요일']}요일: {row['메뉴']} ({row['칼로리']} kcal)",
                          value=st.session_state[key_name],
                          key=key_name)
    
    st.session_state[key_name] = checked
    if checked:
        if row["메뉴"] not in st.session_state["favorites"]:
            st.session_state["favorites"].append(row["메뉴"])
    else:
        if row["메뉴"] in st.session_state["favorites"]:
            st.session_state["favorites"].remove(row["메뉴"])

# ----- 좋아하는 메뉴 표시 -----
if st.session_state["favorites"]:
    st.subheader("선택한 좋아하는 메뉴")
    for fav in st.session_state["favorites"]:
        st.write(f"- {fav}")

# ----- 주간 메뉴 전체 표시 (단순) -----
st.subheader("이번 주 급식")
st.table(df)
