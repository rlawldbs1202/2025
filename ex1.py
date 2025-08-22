import streamlit as st
import pandas as pd
import datetime

st.title("✅ 할 일 관리 앱")
st.write("할 일을 추가하고, 마감일과 함께 진행 상황을 관리하세요!")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state["todos"] = []

# 새로운 할 일 입력
st.subheader("✏️ 새로운 할 일 추가")
task = st.text_input("할 일 입력")
deadline = st.date_input("마감일 선택", datetime.date.today())

if st.button("추가"):
    if task.strip():
        st.session_state["todos"].append(
            {"할 일": task, "마감일": deadline, "완료": False}
        )
        st.success(f"'{task}' 추가 완료!")
    else:
        st.warning("할 일을 입력해주세요!")

# 할 일 목록 표시
if st.session_state["todos"]:
    st.subheader("📋 할 일 목록")

    for i, todo in enumerate(st.session_state["todos"]):
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.session_state["todos"][i]["완료"] = st.checkbox(
                todo["할 일"], value=todo["완료"], key=f"todo_{i}"
            )
        with col2:
            # 마감일 색상 표시 (오늘 이후는 초록, 오늘은 주황, 지난 마감은 빨강)
            if todo["마감일"] < datetime.date.today():
                st.markdown(f"🔴 **{todo['마감일']} (지남)**")
            elif todo["마감일"] == datetime.date.today():
                st.markdown(f"🟠 **{todo['마감일']} (오늘!)**")
            else:
                st.markdown(f"🟢 {todo['마감일']}")
        with col3:
            if st.button("삭제", key=f"delete_{i}"):
                st.session_state["todos"].pop(i)
                st.experimental_rerun()

    # 완료율 계산
    done = sum([1 for t in st.session_state["todos"] if t["완료"]])
    total = len(st.session_state["todos"])
    st.progress(done / total if total > 0 else 0)
    st.write(f"진행률: {done} / {total} 완료 ✅")

    # 테이블 표시
    st.subheader("📊 전체 할 일 테이블")
    df = pd.DataFrame(st.session_state["todos"])
    st.dataframe(df)
else:
    st.info("할 일을 추가해주세요.")

