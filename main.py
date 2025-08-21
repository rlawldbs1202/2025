import streamlit as st

# MBTI별 직업 데이터 (예시)
mbti_jobs = {
    "INFJ": ["상담사", "작가", "교사", "심리학자"],
    "ENFP": ["광고 기획자", "강사", "배우", "마케팅 전문가"],
    "ISTJ": ["회계사", "군인", "경찰관", "데이터 분석가"],
    "ENTP": ["기업가", "기자", "변호사", "스타트업 창업자"],
    # ... 나머지 MBTI도 추가
}

st.title("🌟 MBTI 기반 직업 추천 사이트")
st.write("당신의 MBTI를 선택하면, 어울리는 직업을 추천해드려요!")

# MBTI 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_jobs.keys()))

# 결과 출력
if selected_mbti:
    st.subheader(f"👉 {selected_mbti} 유형에 어울리는 직업")
    for job in mbti_jobs[selected_mbti]:
        st.write(f"- {job}")

