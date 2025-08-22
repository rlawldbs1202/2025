import streamlit as st
import pandas as pd
import datetime

st.title("할 일 관리 앱")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state["todos"] = []

# 할 일 입력
task = st.text_input("할 일")
deadline = st.date_input("마감일", datetime.date.today())

if st.button("추가"):
    if task:
        st.session_state["todos"].append(
            {"할 일": task, "마감일": deadline, "완료": False}
        )

# 할 일 목록 표시
if st.session_state["todos"]:
    for i, todo in enumerate(st.session_state["todos"]):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.session_state["todos"][i]["완료"] = st.checkbox(
                todo["할 일"], value=todo["완료"], key=f"check_{i}"
            )
        with col2:
            st.write(f"{todo['마감일']}")

    # 진행률 표시
    total = len(st.session_state["todos"])
    done = sum(t["완료"] for t in st.session_state["todos"])
    st.write(f"진행률: {done}/{total}")
    st.progress(done / total if total else 0)

    # 테이블 표시
    df = pd.DataFrame(st.session_state["todos"])
    st.dataframe(df)
else:
    st.write("할 일을 추가하세요.")

