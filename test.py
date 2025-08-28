import streamlit as st
import random
from itertools import chain

# 기본 메뉴 (필요 시 언제든 초기화 가능)
DEFAULT_MENUS = {
    "한식": ["김치찌개", "불고기", "비빔밥", "삼겹살", "된장찌개"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "양장피"],
    "일식": ["초밥", "라멘", "돈카츠", "우동", "가츠동"],
    "양식": ["파스타", "스테이크", "피자", "리조또", "샐러드"],
}

st.set_page_config(page_title="저녁 메뉴 추천기", page_icon="🍽️", layout="centered")
st.title("🍽️ 오늘의 저녁 메뉴 추천 앱")

# --- 세션 상태 초기화 ---
if "menu_dict" not in st.session_state:
    # 가변 객체 보호를 위해 복사
    st.session_state.menu_dict = {k: v[:] for k, v in DEFAULT_MENUS.items()}

menu_dict = st.session_state.menu_dict

# 유틸
def all_menus():
    return list(chain.from_iterable(menu_dict.values()))

# --- UI 탭 ---
tab_reco, tab_manage = st.tabs(["🎲 메뉴 추천", "🧰 메뉴 관리"])

# ====== 추천 탭 ======
with tab_reco:
    st.subheader("무엇이 땡기세요?")
    category = st.selectbox("카테고리 선택", ["전체"] + list(menu_dict.keys()), key="sel_category_reco")

    # 후보 리스트 준비
    if category == "전체":
        candidates = all_menus()
    else:
        candidates = menu_dict.get(category, [])[:]

    # 제외할 메뉴 선택(옵션)
    exclude = st.multiselect("제외할 메뉴(선택)", sorted(set(candidates)), key="exclude_menus")
    candidates = [m for m in candidates if m not in exclude]

    col1, col2 = st.columns(2)
    with col1:
        k = st.slider("추천 개수", min_value=1, max_value=5, value=1, step=1, help="최대 5개까지 추천해드려요.")
    with col2:
        allow_dup = st.toggle("중복 허용", value=False, help="체크하면 같은 메뉴가 중복될 수 있어요.")

    if st.button("오늘의 메뉴 추천받기 🎲", use_container_width=True, key="btn_recommend"):
        if not candidates:
            st.warning("추천할 수 있는 메뉴가 없어요. 카테고리를 바꾸거나 제외 메뉴를 줄여보세요.")
        else:
            if allow_dup:
                picks = [random.choice(candidates) for _ in range(k)]
            else:
                # 후보 수가 k보다 적으면 가능한 만큼만 추출
                k_eff = min(k, len(set(candidates)))
                # random.sample은 중복을 허용하지 않으므로 집합 중에서 뽑기
                picks = random.sample(list(set(candidates)), k=k_eff)

            st.success("추천 결과가 나왔어요!")
            for i, p in enumerate(picks, start=1):
                st.markdown(f"**{i}. {p}**")

# ====== 관리 탭 ======
with tab_manage:
    st.subheader("메뉴를 추가/삭제하거나 기본값으로 되돌릴 수 있어요.")

    # 메뉴 추가
    st.markdown("### ➕ 메뉴 추가")
    colA, colB = st.columns([1, 2])
    with colA:
        add_cat = st.selectbox("카테고리", list(menu_dict.keys()), key="sel_category_add")
    with colB:
        new_menu = st.text_input("추가할 메뉴 이름", placeholder="예: 제육볶음", key="txt_new_menu")

    add_clicked = st.button("추가하기", key="btn_add")
    if add_clicked:
        nm = (new_menu or "").strip()
        if not nm:
            st.warning("메뉴 이름을 입력해주세요.")
        else:
            # 중복 체크(대소문자 구분 없이)
            lower_set = {m.lower() for m in menu_dict[add_cat]}
            if nm.lower() in lower_set:
                st.info(f"'{nm}' 는 이미 {add_cat}에 있어요.")
            else:
                menu_dict[add_cat].append(nm)
                st.success(f"✅ '{nm}' 가 {add_cat}에 추가되었습니다!")

    # 메뉴 삭제
    st.markdown("### 🗑️ 메뉴 삭제")
    colC, colD = st.columns([1, 2])
    with colC:
        del_cat = st.selectbox("카테고리", list(menu_dict.keys()), key="sel_category_delete")
    with colD:
        del_targets = st.multiselect("삭제할 메뉴 선택", menu_dict[del_cat], key="multi_delete")

    del_clicked = st.button("선택 메뉴 삭제", key="btn_delete")
    if del_clicked:
        if not del_targets:
            st.warning("삭제할 메뉴를 선택해주세요.")
        else:
            menu_dict[del_cat] = [m for m in menu_dict[del_cat] if m not in del_targets]
            st.success(f"🧹 {len(del_targets)}개 메뉴가 삭제되었습니다.")

    # 현재 메뉴 보기
    with st.expander("📋 현재 메뉴 목록 보기", expanded=False):
        for cat, items in menu_dict.items():
            st.markdown(f"**{cat}** ({len(items)}개)")
            if items:
                st.write(", ".join(items))
            else:
                st.write("_비어 있음_")
            st.divider()

    # 초기화
    if st.button("🔄 전체 메뉴를 기본값으로 되돌리기", type="secondary", key="btn_reset"):
        st.session_state.menu_dict = {k: v[:] for k, v in DEFAULT_MENUS.items()}
        st.success("모든 메뉴가 기본값으로 초기화되었습니다. 상단 탭을 다시 눌러 새로고침해 주세요.")
