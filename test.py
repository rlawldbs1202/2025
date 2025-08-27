import streamlit as st
import random
import itertools

# 기본 메뉴 데이터
menu_dict = {
    "한식": ["김치찌개", "불고기", "비빔밥", "삼겹살", "된장찌개"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "양장피"],
    "일식": ["초밥", "라멘", "돈카츠", "우동", "가츠동"],
    "양식": ["파스타", "스테이크", "피자", "리조또", "샐러드"]
}

st.title("🍽️ 오늘의 저녁 메뉴 추천 앱")

# 카테고리 선택
category = st.selectbox("먹고 싶은 종류를 골라보세요:", ["전체"] + list(menu_dict.keys()))

# 사용자 메뉴 추가 기능
new_menu = st.text_input("추가하고 싶은 메뉴를 입력하세요:")

if st.button("메뉴 추가하기"):
    if category == "전체":
        st.warning("⚠️ '전체' 카테고리에는 메뉴를 직접 추가할 수 없어요. 카테고리를 선택해주세요.")
    elif new_menu.strip() == "":
        st.warning("⚠️ 메뉴 이름을 입력해주세요!")
    else:
        menu_dict[category].append(new_menu.strip())
        st.success(f"✅ '{new_menu}' 가 {category} 메뉴에 추가되었습니다!")

# 추천 버튼
if st.button("오늘의 메뉴 추천받기 🎲"):
    if category == "전체":
        all_menus = list(itertools.chain(*menu_dict.values()))  # 모든 메뉴 합치기
        choice = random.choice(all_menus)
    else:
        choice = random.choice(menu_dict[category])
    st.subheader(f"👉 오늘 저녁은 **{choice}** 어떠세요? 😋")
