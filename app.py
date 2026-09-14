import streamlit as st
import random
import pandas as pd
import os
from datetime import datetime

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="숫자 맞히기 게임",
    page_icon="🎯",
    layout="centered"
)

RANKING_FILE = "ranking.csv"


# =========================================================
# 랭킹 파일 관리
# =========================================================

def load_ranking():
    """랭킹 데이터를 불러옵니다."""

    if not os.path.exists(RANKING_FILE):
        return pd.DataFrame(
            columns=[
                "name",
                "attempts",
                "date"
            ]
        )

    try:
        df = pd.read_csv(RANKING_FILE)

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "name",
                    "attempts",
                    "date"
                ]
            )

        return df

    except Exception:
        return pd.DataFrame(
            columns=[
                "name",
                "attempts",
                "date"
            ]
        )


def save_ranking(name, attempts):
    """새로운 기록을 랭킹에 저장합니다."""

    df = load_ranking()

    new_record = pd.DataFrame(
        [{
            "name": name,
            "attempts": attempts,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }]
    )

    df = pd.concat(
        [df, new_record],
        ignore_index=True
    )

    # 적은 시도 횟수가 높은 순위
    df = df.sort_values(
        by="attempts",
        ascending=True
    )

    # 상위 100명만 저장
    df = df.head(100)

    df.to_csv(
        RANKING_FILE,
        index=False,
        encoding="utf-8-sig"
    )


# =========================================================
# 게임 초기화
# =========================================================

def start_new_game():
    """새 게임을 시작합니다."""

    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.message = "1부터 100 사이의 숫자를 입력하세요."
    st.session_state.history = []


# =========================================================
# 세션 상태 초기화
# =========================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "message" not in st.session_state:
    st.session_state.message = ""

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #4F46E5;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .game-card {
        background-color: #f8f9ff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .score {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #111827;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="main-title">🎯 숫자 맞히기 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">1부터 100 사이의 숫자를 맞혀보세요!</div>',
    unsafe_allow_html=True
)


# =========================================================
# 플레이어 이름
# =========================================================

st.markdown("### 👤 플레이어")

player_name = st.text_input(
    "이름을 입력하세요",
    placeholder="예: 홍길동",
    max_chars=20
)


# =========================================================
# 게임 시작 버튼
# =========================================================

if not st.session_state.game_started:

    st.info(
        "게임을 시작하려면 이름을 입력하고 아래 버튼을 눌러주세요."
    )

    if st.button(
        "🎮 게임 시작",
        use_container_width=True,
        type="primary"
    ):

        if not player_name.strip():
            st.warning("이름을 먼저 입력해주세요.")

        else:
            start_new_game()
            st.rerun()


# =========================================================
# 게임 진행
# =========================================================

if st.session_state.game_started:

    st.markdown("---")

    st.markdown(
        f"""
        <div class="game-card">

        <div class="score">
        👤 {player_name}님의 게임
        </div>

        <div class="score">
        🔢 현재 시도 횟수: {st.session_state.attempts}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # 게임이 끝나지 않은 경우
    if not st.session_state.game_over:

        st.markdown("### 🔢 숫자를 입력하세요")

        guess = st.number_input(
            "1~100 사이의 숫자",
            min_value=1,
            max_value=100,
            value=50,
            step=1
        )

        if st.button(
            "🎯 정답 확인",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.attempts += 1

            secret = st.session_state.secret_number

            # 정답
            if guess == secret:

                st.session_state.game_over = True

                st.session_state.message = (
                    f"🎉 정답입니다! "
                    f"정답은 {secret}입니다."
                )

                # 기록 저장
                save_ranking(
                    player_name.strip(),
                    st.session_state.attempts
                )

                st.balloons()

            # 입력한 숫자가 작음
            elif guess < secret:

                st.session_state.message = (
                    "⬆️ 더 큰 숫자입니다!"
                )

                st.session_state.history.append(
                    {
                        "시도": st.session_state.attempts,
                        "입력": int(guess),
                        "힌트": "더 큰 숫자 ⬆️"
                    }
                )

            # 입력한 숫자가 큼
            else:

                st.session_state.message = (
                    "⬇️ 더 작은 숫자입니다!"
                )

                st.session_state.history.append(
                    {
                        "시도": st.session_state.attempts,
                        "입력": int(guess),
                        "힌트": "더 작은 숫자 ⬇️"
                    }
                )

            st.rerun()

        # 메시지
        if st.session_state.message:

            st.info(
                st.session_state.message
            )

    # =====================================================
    # 게임 종료
    # =====================================================

    else:

        st.success(
            st.session_state.message
        )

        st.markdown(
            f"""
            ### 🏆 최종 기록

            **{player_name}님은 "
            **{st.session_state.attempts}회** 만에 정답을 맞혔습니다!
            """
        )

        if st.button(
            "🔄 다시 게임하기",
            use_container_width=True
        ):

            start_new_game()
            st.rerun()


# =========================================================
# 시도 기록
# =========================================================

if (
    st.session_state.game_started
    and len(st.session_state.history) > 0
):

    st.markdown("---")

    st.markdown("### 📜 나의 시도 기록")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 랭킹
# =========================================================

st.markdown("---")

st.markdown("## 🏆 명예의 전당")

ranking = load_ranking()

if ranking.empty:

    st.info(
        "아직 등록된 기록이 없습니다. "
        "첫 번째 기록을 만들어보세요! 🎯"
    )

else:

    ranking = ranking.sort_values(
        by="attempts",
        ascending=True
    ).head(10)

    ranking_display = []

    for index, row in ranking.reset_index(drop=True).iterrows():

        rank = index + 1

        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        else:
            medal = f"{rank}위"

        ranking_display.append(
            {
                "순위": medal,
                "이름": row["name"],
                "시도 횟수": f"{int(row['attempts'])}회",
                "날짜": row["date"]
            }
        )

    ranking_df = pd.DataFrame(
        ranking_display
    )

    st.table(ranking_df)


# =========================================================
# 게임 규칙
# =========================================================

with st.expander("📖 게임 방법"):

    st.markdown(
        """
        ### 게임 방법

        1. 자신의 이름을 입력합니다.
        2. **게임 시작** 버튼을 누릅니다.
        3. 컴퓨터가 1~100 사이의 숫자를 랜덤으로 정합니다.
        4. 숫자를 입력하고 **정답 확인** 버튼을 누릅니다.
        5. 컴퓨터가 더 큰 숫자인지 작은 숫자인지 알려줍니다.
        6. 정답을 맞힐 때까지 계속 도전합니다.
        7. 적은 횟수로 맞힐수록 높은 순위에 올라갑니다.

        ### 🏆 랭킹 규칙

        **시도 횟수가 적을수록 높은 순위입니다.**

        예:

        - 3회 → 1위
        - 5회 → 2위
        - 7회 → 3위
        """
    )


# =========================================================
# 푸터
# =========================================================

st.markdown("---")

st.caption(
    "🎯 Number Guessing Game · Powered by Streamlit"
)
