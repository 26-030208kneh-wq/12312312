import streamlit as st
import random

from questions import QUESTIONS


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="밸런스 게임",
    page_icon="⚖️",
    layout="centered"
)

MAX_QUESTIONS = 25


# =========================================================
# 세션 상태
# =========================================================

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

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False


# =========================================================
# 질문 가져오기
# =========================================================

def get_questions():

    if st.session_state.category == "전체":
        return QUESTIONS

    return [
        q
        for q in QUESTIONS
        if q["category"] == st.session_state.category
    ]


# =========================================================
# 새로운 질문
# =========================================================

def get_new_question():

    available_questions = get_questions()

    if not available_questions:
        return None

    previous_questions = [
        item["question"]
        for item in st.session_state.history
    ]

    candidates = [
        q
        for q in available_questions
        if q["question"] not in previous_questions
    ]

    if not candidates:
        candidates = available_questions

    return random.choice(candidates)


# =========================================================
# 게임 초기화
# =========================================================

def reset_game():

    st.session_state.score_a = 0
    st.session_state.score_b = 0
    st.session_state.played = 0
    st.session_state.history = []
    st.session_state.game_finished = False

    st.session_state.current_question = get_new_question()


# =========================================================
# 답변 선택
# =========================================================

def select_answer(answer):

    question = st.session_state.current_question

    if question is None:
        return

    # A / B 점수
    if answer == "A":
        st.session_state.score_a += 1
    else:
        st.session_state.score_b += 1

    # 문제 수
    st.session_state.played += 1

    # 기록
    st.session_state.history.append({
        "category": question["category"],
        "question": question["question"],
        "A": question["A"],
        "B": question["B"],
        "answer": answer
    })

    # 25문제 완료
    if st.session_state.played >= MAX_QUESTIONS:

        st.session_state.game_finished = True
        st.session_state.current_question = None

    else:

        st.session_state.current_question = get_new_question()


# =========================================================
# 첫 질문
# =========================================================

if (
    st.session_state.current_question is None
    and not st.session_state.game_finished
):

    st.session_state.current_question = get_new_question()


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 850px;
        padding-top: 40px;
        padding-bottom: 50px;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #222;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .progress-text {
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        color: #444;
        margin: 20px 0;
    }

    .vs-text {
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        color: #888;
        margin: 15px 0;
    }

    .result-title {
        text-align: center;
        font-size: 35px;
        font-weight: 900;
        color: #222;
        margin-top: 20px;
    }

    .result-subtitle {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .choice-label {
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    @media (max-width: 600px) {

        .block-container {
            padding-top: 25px;
        }

        .main-title {
            font-size: 32px;
        }

        .sub-title {
            font-size: 15px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="main-title">⚖️ 밸런스 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">25개의 질문에 답하고 나의 선택을 확인해보세요!</div>',
    unsafe_allow_html=True
)


# =========================================================
# 게임 종료
# =========================================================

if st.session_state.game_finished:

    st.balloons()

    st.markdown(
        '<div class="result-title">🎉 게임 종료!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-subtitle">'
        '25개의 질문을 모두 완료했습니다!'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 점수
    # -----------------------------------------------------

    a_score = st.session_state.score_a
    b_score = st.session_state.score_b

    a_percent = round(
        a_score / MAX_QUESTIONS * 100
    )

    b_percent = round(
        b_score / MAX_QUESTIONS * 100
    )

    st.subheader("📊 나의 선택 결과")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🅰️ A 선택",
            f"{a_score}회"
        )

        st.write(
            f"**{a_percent}%**"
        )

    with col2:

        st.metric(
            "🅱️ B 선택",
            f"{b_score}회"
        )

        st.write(
            f"**{b_percent}%**"
        )

    st.divider()

    # -----------------------------------------------------
    # 선택 비율
    # -----------------------------------------------------

    st.subheader("📈 선택 비율")

    st.progress(a_percent / 100)

    st.write(
        f"🅰️ A **{a_percent}%**"
        f"  　VS　 "
        f"🅱️ B **{b_percent}%**"
    )

    st.divider()

    # -----------------------------------------------------
    # 성향
    # -----------------------------------------------------

    st.subheader("🔮 당신의 선택 성향")

    if a_score >= 21:

        st.success(
            "🅰️ **A 선택 성향이 매우 강합니다!**\n\n"
            "25개의 질문 중 대부분 A를 선택했어요!"
        )

    elif a_score >= 16:

        st.info(
            "🅰️ **A 선택 성향이 강한 편입니다!**\n\n"
            "A를 조금 더 선호하는 스타일이에요."
        )

    elif b_score >= 21:

        st.success(
            "🅱️ **B 선택 성향이 매우 강합니다!**\n\n"
            "25개의 질문 중 대부분 B를 선택했어요!"
        )

    elif b_score >= 16:

        st.info(
            "🅱️ **B 선택 성향이 강한 편입니다!**\n\n"
            "B를 조금 더 선호하는 스타일이에요."
        )

    else:

        st.warning(
            "⚖️ **완벽한 밸런스형!**\n\n"
            "A와 B를 비슷하게 선택했어요!"
        )

    st.divider()

    # -----------------------------------------------------
    # 25개 선택 기록
    # -----------------------------------------------------

    st.subheader("📜 내가 선택한 25개")

    for i, item in enumerate(
        st.session_state.history,
        start=1
    ):

        if item["answer"] == "A":

            selected = item["A"]

            st.write(
                f"**{i}. 🅰️ {selected}**"
            )

        else:

            selected = item["B"]

            st.write(
                f"**{i}. 🅱️ {selected}**"
            )

        st.caption(
            f"{item['category']}  |  {item['question']}"
        )

    st.divider()

    # -----------------------------------------------------
    # 다시하기
    # -----------------------------------------------------

    if st.button(
        "🔄 다시 게임하기",
        use_container_width=True,
        type="primary"
    ):

        reset_game()

        st.rerun()


# =========================================================
# 게임 진행
# =========================================================

else:

    # =====================================================
    # 사이드바
    # =====================================================

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

        # 카테고리 변경
        if (
            selected_category
            != st.session_state.category
        ):

            st.session_state.category = selected_category

            st.session_state.current_question = (
                get_new_question()
            )

        st.divider()

        st.subheader("📊 게임 진행")

        st.write(
            f"🔥 **{st.session_state.played + 1} / {MAX_QUESTIONS}**"
        )

        st.write(
            f"🅰️ A 선택: "
            f"**{st.session_state.score_a}회**"
        )

        st.write(
            f"🅱️ B 선택: "
            f"**{st.session_state.score_b}회**"
        )

        # 진행률
        st.progress(
            st.session_state.played
            / MAX_QUESTIONS
        )

        st.divider()

        if st.button(
            "🔄 게임 초기화",
            use_container_width=True
        ):

            reset_game()

            st.rerun()


    # =====================================================
    # 현재 질문
    # =====================================================

    question = st.session_state.current_question

    if question:

        # -------------------------------------------------
        # 문제 번호
        # -------------------------------------------------

        st.markdown(
            f'<div class="progress-text">'
            f'🔥 {st.session_state.played + 1} / {MAX_QUESTIONS}'
            f'</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 질문 카드
        #
        # 중요:
        # 여기에는 HTML div를 사용하지 않습니다.
        # -------------------------------------------------

        with st.container(border=True):

            st.markdown(
                f"### {question['category']}"
            )

            st.markdown(
                f"## {question['question']}"
            )


        # -------------------------------------------------
        # A / B 버튼
        # -------------------------------------------------

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                '<div class="choice-label">'
                '🅰️ A'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                question["A"],
                key=f"A_{st.session_state.played}",
                use_container_width=True
            ):

                select_answer("A")

                st.rerun()


        with col2:

            st.markdown(
                '<div class="choice-label">'
                '🅱️ B'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                question["B"],
                key=f"B_{st.session_state.played}",
                use_container_width=True
            ):

                select_answer("B")

                st.rerun()


        # -------------------------------------------------
        # VS
        # -------------------------------------------------

        st.markdown(
            '<div class="vs-text">VS</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "💡 정답은 없습니다! 마음에 드는 것을 선택하세요."
        )
