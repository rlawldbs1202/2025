import streamlit as st
import datetime
import uuid

st.title("할 일 관리 앱")

if "todos" not in st.session_state:
    st.session_state["todos"] = []

task = st.text_input("할 일")
deadline = st.date_input("마감일", datetime.date.today())
if st.button("추가") and task:
    st.session_state["todos"].append({"id": str(uuid.uuid4()), "할 일": task, "마감일": deadline, "완료": False})

new_list = []
for todo in st.session_state["todos"]:
    c1, c2, c3 = st.columns([3, 2, 1])
    done = c1.checkbox(todo["할 일"], value=todo["완료"], key=todo["id"])
    c2.write(todo["마감일"])
    remove = c3.button("삭제", key=f"del_{todo['id']}")
    if not remove:
        new_list.append({"id": todo["id"], "할 일": todo["할 일"], "마감일": todo["마감일"], "완료": done})
st.session_state["todos"] = new_list

st.write(f"진행률: {sum(t['완료'] for t in new_list)}/{len(new_list)}")
