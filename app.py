import streamlit as st
import random
from questions import QUESTIONS


# ==========================================
# 페이지 설정
# ==========================================

st.set_page_config(
    page_title="밸런스 게임 ⚖️",
    page_icon="⚖️",
    layout="centered"
)


# ==========================================
# 게임 설정
# ==========================================

MAX_QUESTIONS = 25


# ==========================================
# 세션 상태 초기화
# ==========================================

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


# ==========================================
# 질문 가져오기
# ==========================================

def get_questions():

    if st.session_state.category == "전체":
        return QUESTIONS

    return [
        q for q in QUESTIONS
        if q["category"] == st.session_state.category
    ]


# ==========================================
# 새로운 질문 가져오기
# ==========================================

def get_new_question():

    available_questions = get_questions()

    if not available_questions:
        return None

    previous_questions = [
        item["question"]
        for item in st.session_state.history
    ]

    candidates = [
        q for q in available_questions
        if q["question"] not in previous_questions
    ]

    if not candidates:
        candidates = available_questions

    return random.choice(candidates)


# ==========================================
# 게임 초기화
# ==========================================

def reset_game():

    st.session_state.current_question = None
    st.session_state.score_a = 0
    st.session_state.score_b = 0
    st.session_state.played = 0
    st.session_state.history = []
    st.session_state.game_finished = False

    st.session_state.current_question = get_new_question()


# ==========================================
# 답변 선택
# ==========================================

def select_answer(answer):

    question = st.session_state.current_question

    if question is None:
        return

    # 점수 기록
    if answer == "A":
        st.session_state.score_a += 1
    else:
        st.session_state.score_b += 1

    # 문제 수 증가
    st.session_state.played += 1

    # 기록 저장
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


# ==========================================
# 첫 질문 생성
# ==========================================

if (
    st.session_state.current_question is None
    and not st.session_state.game_finished
):
    st.session_state.current_question = get_new_question()


# ==========================================
# CSS
# ==========================================

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

        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.12);
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

    .progress-text {
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        margin: 15px 0;
    }

    .result-box {
        background: linear-gradient(
            135deg,
            #667eea,
            #764ba2
        );

        color: white;
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        margin-top: 30px;

        box-shadow:
            0 15px 35px rgba(0,0,0,0.18);
    }

    .result-title {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .result-score {
        font-size: 22px;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 제목
# ==========================================

st.markdown(
    '<div class="main-title">⚖️ 밸런스 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">25개의 질문에 답하고 나의 선택을 확인해보세요!</div>',
    unsafe_allow_html=True
)


# ==========================================
# 게임 종료 화면
# ==========================================

if st.session_state.game_finished:

    st.balloons()

    st.markdown(
        """
        <div class="result-box">

            <div class="result-title">
                🎉 게임 종료!
            </div>

            <div class="result-score">
                25개의 질문을 모두 완료했습니다!<br>
                당신의 밸런스 게임 결과를 확인해보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------
    # 결과 계산
    # --------------------------------------

    a_score = st.session_state.score_a
    b_score = st.session_state.score_b

    a_percent = round(
        (a_score / MAX_QUESTIONS) * 100
    )

    b_percent = round(
        (b_score / MAX_QUESTIONS) * 100
    )

    st.subheader("📊 나의 선택 결과")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🅰️ A 선택",
            f"{a_score}회",
            f"{a_percent}%"
        )

    with col2:

        st.metric(
            "🅱️ B 선택",
            f"{b_score}회",
            f"{b_percent}%"
        )

    st.divider()

    # --------------------------------------
    # 성향 결과
    # --------------------------------------

    st.subheader("🔮 당신의 선택 성향")

    if a_score >= 20:

        st.success(
            "🅰️ **A 선택 성향이 매우 강합니다!**\n\n"
            "당신은 확실한 선택을 좋아하는 스타일이에요."
        )

    elif a_score >= 15:

        st.info(
            "🅰️ **A 선택 성향이 강한 편입니다!**\n\n"
            "전체적으로 A를 선호하는 모습을 보여줬어요."
        )

    elif b_score >= 20:

        st.success(
            "🅱️ **B 선택 성향이 매우 강합니다!**\n\n"
            "당신은 자신만의 확실한 취향이 있는 스타일이에요."
        )

    elif b_score >= 15:

        st.info(
            "🅱️ **B 선택 성향이 강한 편입니다!**\n\n"
            "전체적으로 B를 선호하는 모습을 보여줬어요."
        )

    else:

        st.warning(
            "⚖️ **완벽한 밸런스형!**\n\n"
            "A와 B를 비슷하게 선택했어요. "
            "상황에 따라 유연하게 선택하는 스타일입니다!"
        )

    st.divider()

    # --------------------------------------
    # 내가 선택한 기록
    # --------------------------------------

    st.subheader("📜 내가 선택한 25개")

    for i, item in enumerate(
        st.session_state.history,
        start=1
    ):

        if item["answer"] == "A":
            selected = f"🅰️ {item['A']}"
        else:
            selected = f"🅱️ {item['B']}"

        st.write(
            f"**{i}. {item['question']}**"
        )

        st.caption(
            f"{item['category']}  |  선택: {selected}"
        )

    st.divider()

    # --------------------------------------
    # 다시하기
    # --------------------------------------

    if st.button(
        "🔄 다시 게임하기",
        use_container_width=True
    ):

        reset_game()

        st.rerun()


# ==========================================
# 게임 진행 화면
# ==========================================

else:

    # --------------------------------------
    # 사이드바
    # --------------------------------------

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
            f"문제: **{st.session_state.played + 1} / {MAX_QUESTIONS}**"
        )

        st.write(
            f"🅰️ A 선택: **{st.session_state.score_a}회**"
        )

        st.write(
            f"🅱️ B 선택: **{st.session_state.score_b}회**"
        )

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


    # --------------------------------------
    # 문제
    # --------------------------------------

    question = st.session_state.current_question

    if question:

        # 진행 상황
        st.markdown(
            f"""
            <div class="progress-text">
                🔥 {st.session_state.played + 1} / {MAX_QUESTIONS}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 질문
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

        st.write("")

        # ----------------------------------
        # 선택 버튼
        # ----------------------------------

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

        st.write("")

        st.caption(
            "💡 정답은 없습니다! 마음에 드는 것을 선택하세요."
        )
