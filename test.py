import streamlit as st
import pandas as pd
import datetime
import uuid

st.title("할 일 관리 앱")

if "todos" not in st.session_state:
    st.session_state["todos"] = []

task = st.text_input("할 일")
deadline = st.date_input("마감일", datetime.date.today())

if st.button("추가"):
    if task:
        st.session_state["todos"].append(
            {"id": str(uuid.uuid4()), "할 일": task, "마감일": deadline, "완료": False}
        )

if st.session_state["todos"]:
    new_todos = []
    for todo in st.session_state["todos"]:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            done = st.checkbox(todo["할 일"], value=todo["완료"], key=todo["id"])
        with col2:
            st.write(str(todo["마감일"]))
        with col3:
            remove = st.button("삭제", key=f"del_{todo['id']}")

        if not remove:
            new_todos.append({"id": todo["id"], "할 일": todo["할 일"], "마감일": todo["마감일"], "완료": done})

    st.session_state["todos"] = new_todos

    total = len(st.session_state["todos"])
    done_count = sum(t["완료"] for t in st.session_state["todos"])
    st.progress(done_count / total if total else 0)
    st.write(f"진행률: {done_count}/{total}")

    df = pd.DataFrame(st.session_state["todos"])
    st.dataframe(df)

