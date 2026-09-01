import streamlit as st
import random
from questions import QUESTIONS


# ---------------------------------------
# 기본 설정
# ---------------------------------------

st.set_page_config(
    page_title="밸런스 게임 🎮",
    page_icon="⚖️",
    layout="centered"
)


# ---------------------------------------
# 세션 상태 초기화
# ---------------------------------------

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "score_a" not in st.session_state:
    st.session_state.score_a = 0

if "score_b" not in st.session_state:
    st.session_state.score_b = 0

if "played" not in st.session_state:
    st.session_state.played = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "category" not in st.session_state:
    st.session_state.category = "전체"


# ---------------------------------------
# 질문 가져오기
# ---------------------------------------

def get_questions():
    """선택된 카테고리에 맞는 질문을 반환"""

    if st.session_state.category == "전체":
        return QUESTIONS

    return [
        q for q in QUESTIONS
        if q["category"] == st.session_state.category
    ]


def get_new_question():
    """새로운 질문을 랜덤으로 가져오기"""

    available_questions = get_questions()

    if not available_questions:
        return None

    # 이전 질문과 겹치지 않도록 시도
    previous_questions = [
        item["question"]
        for item in st.session_state.history
    ]

    candidates = [
        q for q in available_questions
        if q["question"] not in previous_questions
    ]

    # 모든 문제를 한 번씩 풀었다면 다시 전체에서 선택
    if not candidates:
        candidates = available_questions

    return random.choice(candidates)


# ---------------------------------------
# 선택 처리
# ---------------------------------------

def select_answer(answer):
    question = st.session_state.current_question

    if question is None:
        return

    if answer == "A":
        st.session_state.score_a += 1
    else:
        st.session_state.score_b += 1

    st.session_state.played += 1

    st.session_state.history.append({
        "category": question["category"],
        "question": question["question"],
        "A": question["A"],
        "B": question["B"],
        "answer": answer
    })

    st.session_state.current_question = get_new_question()


# ---------------------------------------
# 첫 질문 생성
# ---------------------------------------

if st.session_state.current_question is None:
    st.session_state.current_question = get_new_question()


# ---------------------------------------
# CSS
# ---------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .question-box {
        background: linear-gradient(
            135deg,
            #667eea 0%,
            #764ba2 100%
        );

        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    .question-category {
        font-size: 15px;
        opacity: 0.85;
        margin-bottom: 10px;
    }

    .question-text {
        font-size: 25px;
        font-weight: 700;
    }

    .vs {
        text-align: center;
        font-size: 25px;
        font-weight: 800;
        color: #888;
        margin-top: 20px;
    }

    .score-box {
        background-color: #f7f7f7;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# 제목
# ---------------------------------------

st.markdown(
    '<div class="main-title">⚖️ 밸런스 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">둘 중 하나만 선택할 수 있다면?</div>',
    unsafe_allow_html=True
)


# ---------------------------------------
# 사이드바
# ---------------------------------------

with st.sidebar:

    st.header("🎯 게임 설정")

    categories = [
        "전체",
        "🎮 게임",
        "🍔 음식",
        "✈️ 여행지",
        "🎤 아이돌",
        "🎵 노래",
        "🎬 영화/드라마",
        "💰 돈/라이프",
        "💖 연애"
    ]

    selected_category = st.selectbox(
        "카테고리",
        categories,
        index=categories.index(
            st.session_state.category
        )
    )

    if selected_category != st.session_state.category:
        st.session_state.category = selected_category
        st.session_state.current_question = get_new_question()

    st.divider()

    st.subheader("📊 현재 기록")

    st.write(
        f"🎮 플레이: **{st.session_state.played}문제**"
    )

    st.write(
        f"🅰️ A 선택: **{st.session_state.score_a}회**"
    )

    st.write(
        f"🅱️ B 선택: **{st.session_state.score_b}회**"
    )

    st.divider()

    if st.button(
        "🔄 게임 초기화",
        use_container_width=True
    ):
        st.session_state.current_question = get_new_question()
        st.session_state.score_a = 0
        st.session_state.score_b = 0
        st.session_state.played = 0
        st.session_state.history = []

        st.rerun()


# ---------------------------------------
# 현재 질문
# ---------------------------------------

question = st.session_state.current_question


if question:

    st.markdown(
        f"""
        <div class="question-box">

            <div class="question-category">
                {question["category"]}
            </div>

            <div class="question-text">
                {question["question"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------
    # 선택지
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🅰️ A")

        if st.button(
            question["A"],
            key="answer_a",
            use_container_width=True
        ):
            select_answer("A")
            st.rerun()


    with col2:

        st.markdown("### 🅱️ B")

        if st.button(
            question["B"],
            key="answer_b",
            use_container_width=True
        ):
            select_answer("B")
            st.rerun()


    st.markdown(
        '<div class="vs">VS</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------
# 점수 표시
# ---------------------------------------

st.markdown(
    f"""
    <div class="score-box">

    <b>📊 나의 선택 기록</b>

    <br><br>

    🅰️ A 선택
    <b>{st.session_state.score_a}</b>
    회

    &nbsp;&nbsp;&nbsp;

    🅱️ B 선택
    <b>{st.session_state.score_b}</b>
    회

    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# 선택 기록
# ---------------------------------------

if st.session_state.history:

    with st.expander("📜 내가 지금까지 선택한 기록 보기"):

        for i, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            answer_text = (
                item["A"]
                if item["answer"] == "A"
                else item["B"]
            )

            st.write(
                f"**{i}. [{item['category']}]** "
                f"{item['question']}"
            )

            st.write(
                f"👉 선택: **{answer_text}**"
            )

            st.divider()


# ---------------------------------------
# 하단 안내
# ---------------------------------------

st.caption(
    "💡 정답은 없습니다. 당신의 취향을 선택해보세요!"
)
