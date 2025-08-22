import streamlit as st
import pandas as pd
import datetime

st.title("✅ 할 일 관리 앱")
st.write("오늘의 할 일을 추가하고, 마감일과 함께 관리하세요!")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state["todos"] = []

# 새로운 할 일 입력
with st.form("new_task_form", clear_on_submit=True):
    task = st.text_input("할 일 입력")
    deadline = st.date_input("마감일 선택", datetime.date.today())
    submitted = st.form_submit_button("추가")

    if submitted:
        if task.strip() != "":
            st.session_state["todos"].append(
                {"할 일": task, "마감일": deadline, "완료": False}
            )
            st.success("할 일이 추가되었습니다!")
        else:
            st.warning("내용을 입력해주세요!")

# 할 일 목록 표시
if st.session_state["todos"]:
    st.subheader("📋 할 일 목록")

    for i, todo in enumerate(st.session_state["todos"]):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            checked = st.checkbox(todo["할 일"], value=todo["완료"], key=f"check_{i}")
        with col2:
            st.write(f"⏰ {todo['마감일']}")
        with col3:
            if st.button("삭제", key=f"delete_{i}"):
                st.session_state["todos"].pop(i)
                st.experimental_rerun()

        st.session_state["todos"][i]["완료"] = checked

    # 완료율 계산
    done = sum([1 for t in st.session_state["todos"] if t["완료"]])
    total = len(st.session_state["todos"])
    st.progress(done / total if total > 0 else 0)
    st.write(f"진행률: {done} / {total} 완료 ✅")

    # DataFrame 보기
    st.subheader("📊 전체 할 일 테이블")
    st.dataframe(pd.DataFrame(st.session_state["todos"]))
else:
    st.info("할 일을 추가해주세요.")

