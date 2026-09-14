import random
import streamlit as st
from database import init_db, save_score, get_ranking


# ---------------------------------------
# 기본 설정
# ---------------------------------------

st.set_page_config(
    page_title="숫자 맞히기 게임",
    page_icon="🎯",
    layout="centered"
)

init_db()


# ---------------------------------------
# CSS
# ---------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #4F46E5;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #f0f2f6;
        text-align: center;
        margin: 20px 0;
    }

    .ranking-title {
        text-align: center;
        color: #4F46E5;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# 세션 상태 초기화
# ---------------------------------------

if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = ""

if "score_saved" not in st.session_state:
    st.session_state.score_saved = False


# ---------------------------------------
# 제목
# ---------------------------------------

st.markdown(
    '<div class="main-title">🎯 숫자 맞히기 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">1부터 100 사이의 숫자를 맞혀보세요!</div>',
    unsafe_allow_html=True
)


# ---------------------------------------
# 플레이어 이름
# ---------------------------------------

player_name = st.text_input(
    "👤 플레이어 이름",
    placeholder="이름을 입력하세요"
)


# ---------------------------------------
# 게임 정보
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎯 도전 횟수",
        st.session_state.attempts
    )

with col2:
    st.metric(
        "🔢 범위",
        "1 ~ 100"
    )


# ---------------------------------------
# 숫자 입력
# ---------------------------------------

if not st.session_state.game_over:

    guess = st.number_input(
        "숫자를 입력하세요",
        min_value=1,
        max_value=100,
        value=50,
        step=1
    )

    if st.button(
        "🎯 정답 확인",
        use_container_width=True
    ):

        if not player_name.strip():
            st.warning("먼저 플레이어 이름을 입력해주세요.")

        else:

            st.session_state.attempts += 1

            # 정답
            if guess == st.session_state.target_number:

                st.session_state.game_over = True

                attempts = st.session_state.attempts

                # 점수 계산
                score = max(
                    1000 - ((attempts - 1) * 100),
                    100
                )

                st.session_state.score = score

                st.session_state.message = (
                    f"🎉 정답입니다! "
                    f"{attempts}번 만에 맞혔습니다."
                )

                # 점수 저장
                if not st.session_state.score_saved:

                    save_score(
                        player_name.strip(),
                        score,
                        attempts
                    )

                    st.session_state.score_saved = True

                st.success(
                    st.session_state.message
                )

                st.balloons()

            # 입력값이 작음
            elif guess < st.session_state.target_number:

                st.warning(
                    "⬆️ 정답은 더 큰 숫자입니다!"
                )

            # 입력값이 큼
            else:

                st.warning(
                    "⬇️ 정답은 더 작은 숫자입니다!"
                )


# ---------------------------------------
# 게임 종료 화면
# ---------------------------------------

if st.session_state.game_over:

    st.markdown(
        f"""
        <div class="result-box">
            <h2>🎉 게임 클리어!</h2>
            <p>정답: <strong>{st.session_state.target_number}</strong></p>
            <p>도전 횟수: <strong>{st.session_state.attempts}회</strong></p>
            <p>점수: <strong>{st.session_state.score}점</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔄 새 게임 시작",
        use_container_width=True
    ):

        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.message = ""
        st.session_state.score_saved = False
        st.session_state.score = 0

        st.rerun()


# ---------------------------------------
# 랭킹
# ---------------------------------------

st.divider()

st.markdown(
    '<h2 class="ranking-title">🏆 TOP 10 랭킹</h2>',
    unsafe_allow_html=True
)

ranking = get_ranking()

if ranking:

    for index, player in enumerate(ranking, start=1):

        name = player["name"]
        score = player["score"]
        attempts = player["attempts"]

        if index == 1:
            medal = "🥇"
        elif index == 2:
            medal = "🥈"
        elif index == 3:
            medal = "🥉"
        else:
            medal = f"{index}."

        col1, col2, col3 = st.columns([1, 4, 2])

        with col1:
            st.write(f"### {medal}")

        with col2:
            st.write(f"**{name}**")

        with col3:
            st.write(
                f"{score}점 ({attempts}회)"
            )

else:

    st.info(
        "아직 기록이 없습니다. 첫 번째 랭킹 주인공이 되어보세요! 🎯"
    )
