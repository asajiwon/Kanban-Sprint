import streamlit as st
import pandas as pd
from datetime import date

CSV_PATH = "projects.csv"

# 데이터 로딩
@st.cache_data
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame(columns=["제목", "시작일", "마감일", "상태", "진행률", "태스크"])

# 데이터 저장
def save_data(df):
    df.to_csv(CSV_PATH, index=False)

st.set_page_config(page_title="📋 프로젝트 관리 보드", layout="wide")
st.title("📋 프로젝트 관리 보드")

# 데이터 불러오기
df = load_data()

# 새 프로젝트 추가 폼
with st.form("add_project_form"):
    st.subheader("➕ 새 프로젝트 추가")
    title = st.text_input("프로젝트 제목")
    start_date = st.date_input("시작일", value=date.today())
    due_date = st.date_input("마감일")
    status = st.selectbox("상태", ["대기 중", "진행중", "완료"])
    tasks = st.text_area("태스크 (체크박스 형식으로 작성)", "- [ ] 예시 태스크 1\n- [ ] 예시 태스크 2")
    submitted = st.form_submit_button("✅ 추가")
    if submitted and title:
        new_row = pd.DataFrame([[title, start_date, due_date, status, 0, tasks]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("프로젝트가 추가되었습니다.")

st.markdown("---")
st.subheader("📊 전체 프로젝트 목록")
st.dataframe(df, use_container_width=True)

# 상태별 칸반 형태 출력
with st.expander("📌 상태별 보기 (칸반 스타일)"):
    status_columns = st.columns(3)
    status_labels = ["대기 중", "진행중", "완료"]
    for col, label in zip(status_columns, status_labels):
        with col:
            st.markdown(f"### {label}")
            filtered = df[df["상태"] == label]
            for _, row in filtered.iterrows():
                st.markdown(f"**{row['제목']}**\n\n🗓️ {row['시작일']} ~ {row['마감일']}\n\n📈 진행률: {row['진행률']}%\n\n{row['태스크']}")
