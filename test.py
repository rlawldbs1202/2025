import streamlit as st
import pandas as pd

st.title("급식 메뉴 앱")
st.write("오늘과 이번 주 급식 메뉴를 확인하고, 좋아하는 메뉴를 체크해보세요.")

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

# ----- 오늘 메뉴 (예시: 월요일) -----
st.subheader("오늘의 급식")
today_menu = df.iloc[0]  # 실제 앱에서는 datetime으로 요일 자동 선택 가능
st.write(f"메뉴: {today_menu['메뉴']}")
st.write(f"칼로리: {today_menu['칼로리']} kcal")

# ----- 좋아하는 메뉴 체크 -----
st.subheader("좋아하는 메뉴 선택")
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

for i, row in df.iterrows():
    checked = st.checkbox(f"{row['요일']}요일: {row['메뉴']} ({row['칼로리']} kcal)",
                          key=f"menu_{i}")
    if checked and row["메뉴"] not in st.session_state["favorites"]:
        st.session_state["favorites"].append(row["메뉴"])
    elif not checked and row["메뉴"] in st.session_state["favorites"]:
        st.session_state["favorites"].remove(row["메뉴"])

# ----- 좋아하는 메뉴 표시 -----
if st.session_state["favorites"]:
    st.subheader("선택한 좋아하는 메뉴")
    for fav in st.session_state["favorites"]:
        st.write(f"- {fav}")

# ----- 주간 메뉴 표 -----
st.subheader("이번 주 급식")
st.dataframe(df)
