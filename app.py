import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# CAMO | Cathode Advanced Material Optimizer
# Futuristic Battery Materials Research Institute
# =========================================================

st.set_page_config(
    page_title="CAMO | Research Institute",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #123d52 0%, transparent 35%),
        linear-gradient(135deg, #06101c, #0b1b2b 55%, #081522);
    color: #e8f4fb;
}
section[data-testid="stSidebar"] {
    background: #091827;
    border-right: 1px solid #24516a;
}
section[data-testid="stSidebar"] * {
    color: #d8eaf4;
}
h1, h2, h3 {
    color: #eaf7ff;
}
.lab-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #64e6d8;
}
.lab-subtitle {
    color: #9ebdce;
    letter-spacing: 2px;
    font-size: 12px;
}
.hero {
    background: linear-gradient(115deg, rgba(14,47,68,.97), rgba(12,77,88,.72));
    border: 1px solid #28778a;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 22px;
    box-shadow: 0 0 28px rgba(32, 194, 190, .08);
}
.panel {
    background: rgba(17, 40, 58, .92);
    border: 1px solid #28516a;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.room-card {
    background: linear-gradient(145deg, #102b40, #0c1c2d);
    border: 1px solid #2c647b;
    border-radius: 15px;
    padding: 20px;
    min-height: 150px;
}
.room-code {
    font-family: 'Orbitron', sans-serif;
    color: #5de2d4;
    font-size: 12px;
    letter-spacing: 2px;
}
.room-name {
    color: #f0faff;
    font-size: 19px;
    font-weight: 700;
    margin-top: 9px;
}
.room-desc {
    color: #a8c1d0;
    font-size: 13px;
    margin-top: 7px;
}
div[data-testid="stMetric"] {
    background: rgba(16, 42, 60, .9);
    border: 1px solid #28516a;
    border-radius: 12px;
    padding: 13px;
}
.stButton > button {
    background: linear-gradient(90deg, #087e8b, #13a99b);
    color: white;
    border: 1px solid #39b8b1;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
    width: 100%;
}
.stButton > button:hover {
    background: #35d2c0;
    color: #071522;
    border-color: #74fff0;
}
div[data-baseweb="select"] > div {
    background: #10283a;
}
.stProgress > div > div > div {
    background-color: #43d6c5;
}
hr {
    border-color: #25465b;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #28516a;
    border-radius: 10px;
}
.notice {
    border-left: 3px solid #e7b75c;
    background: rgba(112, 83, 28, .16);
    padding: 12px 15px;
    border-radius: 5px;
    color: #e9d5a8;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- MATERIAL DATABASE --------------------
# All values below are illustrative educational data.
# Replace with literature-backed data before scientific use.

DATA = pd.DataFrame([
    {
        "소재": "LFP",
        "화학식": "LiFePO4",
        "에너지밀도": 160,
        "수명": 3000,
        "안전성": 95,
        "원가": 35,
        "출력특성": 75,
        "자원안정성": 95,
        "설명": "인산철계 양극재. 높은 안전성과 긴 수명이 특징인 소재."
    },
    {
        "소재": "NCM111",
        "화학식": "LiNi1/3Co1/3Mn1/3O2",
        "에너지밀도": 180,
        "수명": 1500,
        "안전성": 75,
        "원가": 65,
        "출력특성": 80,
        "자원안정성": 65,
        "설명": "니켈·코발트·망간 비율이 1:1:1인 삼원계 양극재."
    },
    {
        "소재": "NCM622",
        "화학식": "LiNi0.6Co0.2Mn0.2O2",
        "에너지밀도": 200,
        "수명": 1200,
        "안전성": 65,
        "원가": 75,
        "출력특성": 85,
        "자원안정성": 55,
        "설명": "니켈 비율이 높은 삼원계 양극재."
    },
    {
        "소재": "NCM811",
        "화학식": "LiNi0.8Co0.1Mn0.1O2",
        "에너지밀도": 220,
        "수명": 1000,
        "안전성": 55,
        "원가": 85,
        "출력특성": 90,
        "자원안정성": 45,
        "설명": "높은 니켈 함량을 통해 에너지밀도를 높인 양극재."
    },
    {
        "소재": "LMFP",
        "화학식": "LiMn0.5Fe0.5PO4",
        "에너지밀도": 180,
        "수명": 2500,
        "안전성": 90,
        "원가": 45,
        "출력특성": 78,
        "자원안정성": 90,
        "설명": "망간과 철을 활용한 인산염계 양극재."
    }
])

CRITERIA = {
    "에너지밀도": "benefit",
    "수명": "benefit",
    "안전성": "benefit",
    "원가": "cost",
    "출력특성": "benefit",
    "자원안정성": "benefit"
}

ROOMS = {
    "중앙 통제실": "COMMAND CENTER",
    "소재 분석 연구실": "MATERIALS LAB",
    "배터리 실험실": "BATTERY TESTING LAB",
    "AI 분석 센터": "AI ANALYSIS CENTER",
    "연구 기록 보관소": "RESEARCH ARCHIVE"
}


# -------------------- SESSION DATA --------------------

defaults = {
    "xp": 0,
    "completed": [],
    "history": [],
    "experiment_count": 0,
    "latest_ranking": None,
    "latest_pareto": None,
    "latest_sensitivity": None,
    "latest_experiment": None,
    "room": "중앙 통제실"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def award_xp(activity, amount):
    if activity in st.session_state.completed:
        return False

    st.session_state.completed.append(activity)
    st.session_state.xp += amount
    st.session_state.history.append({
        "활동": activity,
        "획득 경험치": amount,
        "기록 시간": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    return True


def get_level():
    xp = st.session_state.xp
    return xp // 100 + 1, xp % 100


# -------------------- ANALYSIS ENGINE --------------------

def normalize_data(df):
    normalized = pd.DataFrame(index=df.index)

    for column, direction in CRITERIA.items():
        values = df[column].astype(float)
        minimum = values.min()
        maximum = values.max()

        if maximum == minimum:
            normalized[column] = 1.0
        elif direction == "benefit":
            normalized[column] = (
                (values - minimum) / (maximum - minimum)
            )
        else:
            normalized[column] = (
                (maximum - values) / (maximum - minimum)
            )

    return normalized


def optimize_materials(df, weights):
    normalized = normalize_data(df)
    total_weight = sum(weights.values())

    if total_weight <= 0:
        raise ValueError("평가 가중치의 합은 0보다 커야 합니다.")

    scores = pd.Series(0.0, index=df.index)

    for column, weight in weights.items():
        scores += normalized[column] * weight / total_weight

    result = pd.DataFrame({
        "소재": df["소재"],
        "종합점수": scores * 100
    })

    result = result.sort_values(
        "종합점수", ascending=False
    ).reset_index(drop=True)

    result.insert(0, "순위", range(1, len(result) + 1))
    return result


def pareto_analysis(df):
    normalized = normalize_data(df)
    matrix = normalized[list(CRITERIA.keys())].to_numpy()

    efficient = []

    for i in range(len(matrix)):
        dominated = False

        for j in range(len(matrix)):
            if i == j:
                continue

            if (
                np.all(matrix[j] >= matrix[i])
                and np.any(matrix[j] > matrix[i])
            ):
                dominated = True
                break

        efficient.append(not dominated)

    result = df[["소재"]].copy()
    result["파레토 최적 후보"] = efficient
    return result


def make_sensitivity(df, selected_criterion, base_weights):
    records = []

    for change in [-40, -20, 0, 20, 40]:
        weights = base_weights.copy()
        weights[selected_criterion] = max(
            0.1,
            base_weights[selected_criterion] * (1 + change / 100)
        )

        ranking = optimize_materials(df, weights)

        for _, row in ranking.iterrows():
            records.append({
                "가중치 변화": change,
                "소재": row["소재"],
                "순위": row["순위"]
            })

    return pd.DataFrame(records)


def radar_chart(df, selected):
    categories = list(CRITERIA.keys())
    fig = go.Figure()

    for material in selected:
        row = df[df["소재"] == material].iloc[0]
        values = []

        for category in categories:
            col = df[category]
            if col.max() == col.min():
                value = 1
            elif CRITERIA[category] == "benefit":
                value = (row[category] - col.min()) / (
                    col.max() - col.min()
                )
            else:
                value = (col.max() - row[category]) / (
                    col.max() - col.min()
                )
            values.append(value)

        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=material
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor="#36556b"
            ),
            bgcolor="#102337"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e6f3fa",
        legend=dict(orientation="h"),
        margin=dict(l=35, r=35, t=35, b=35)
    )
    return fig


# -------------------- COMMON UI --------------------

level, progress = get_level()

with st.sidebar:
    st.markdown(
        '<div class="lab-title">CAMO</div>'
        '<div class="lab-subtitle">ADVANCED MATERIALS INSTITUTE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### INSTITUTE NAVIGATION")

    room = st.radio(
        "연구 시설",
        list(ROOMS.keys()),
        key="room"
    )

    st.divider()

    st.markdown("### RESEARCHER PROFILE")
    st.metric("연구원 등급", f"LEVEL {level}")
    st.progress(progress / 100)
    st.caption(
        f"경험치 {st.session_state.xp} XP · "
        f"다음 등급까지 {100-progress} XP"
    )

    st.divider()
    st.markdown("### INSTITUTE STATUS")
    st.caption("● 시스템 정상 작동")
    st.caption(f"등록 소재: {len(DATA)}종")
    st.caption(f"수행 연구: {len(st.session_state.completed)}개")

    st.divider()
    st.caption("CAMO RESEARCH SYSTEM / v2.0")


def page_header(code, title, description):
    st.markdown(
        f"""
        <div class="hero">
            <div class="room-code">{code}</div>
            <h1>{title}</h1>
            <div style="color:#b3cedd">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def room_button(label, target, key):
    if st.button(label, key=key, use_container_width=True):
        st.session_state.room = target
        st.rerun()


# =========================================================
# ROOM 1 : COMMAND CENTER
# =========================================================

if room == "중앙 통제실":

    page_header(
        "INSTITUTE MAIN CONTROL",
        "중앙 통제실",
        "CAMO 연구소의 전체 연구 현황과 실험 시설을 관리하는 공간입니다."
    )

    st.subheader("INSTITUTE OVERVIEW")

    a, b, c, d = st.columns(4)
    a.metric("등록 양극재", f"{len(DATA)}종")
    b.metric("연구원 등급", f"LEVEL {level}")
    c.metric("누적 경험치", f"{st.session_state.xp} XP")
    d.metric("완료 연구", f"{len(st.session_state.completed)}건")

    st.divider()

    st.subheader("RESEARCH FACILITIES")

    facility_data = [
        (
            "01",
            "소재 분석 연구실",
            "양극재의 화학적 특성과 물성 데이터를 분석합니다.",
            "소재 분석 연구실"
        ),
        (
            "02",
            "배터리 실험실",
            "온도와 충전 조건을 설정하고 가상 실험을 수행합니다.",
            "배터리 실험실"
        ),
        (
            "03",
            "AI 분석 센터",
            "다기준 최적화와 파레토 및 민감도 분석을 수행합니다.",
            "AI 분석 센터"
        ),
        (
            "04",
            "연구 기록 보관소",
            "연구 이력과 분석 결과를 확인하고 보고서를 저장합니다.",
            "연구 기록 보관소"
        )
    ]

    for i in range(0, len(facility_data), 2):
        cols = st.columns(2)

        for col, item in zip(cols, facility_data[i:i+2]):
            number, title, description, target = item

            with col:
                st.markdown(
                    f"""
                    <div class="room-card">
                        <div class="room-code">FACILITY {number}</div>
                        <div class="room-name">{title}</div>
                        <div class="room-desc">{description}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                room_button(
                    f"{title} 입장 →",
                    target,
                    f"enter_{number}"
                )

    st.divider()

    st.subheader("RECENT RESEARCH ACTIVITY")

    if st.session_state.history:
        st.dataframe(
            pd.DataFrame(st.session_state.history).tail(5),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("아직 기록된 연구 활동이 없습니다.")

    st.markdown(
        '<div class="notice">연구 데이터 안내: 현재 기본 데이터는 '
        '프로그램 기능을 보여주기 위한 교육용 예시값입니다. '
        '실제 연구 결과로 해석하면 안 됩니다.</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ROOM 2 : MATERIALS LAB
# =========================================================

elif room == "소재 분석 연구실":

    page_header(
        "FACILITY 01 / MATERIAL CHARACTERIZATION",
        "소재 분석 연구실",
        "이차전지 양극재의 구성과 주요 성능 특성을 비교합니다."
    )

    st.subheader("MATERIAL DATABASE")

    search = st.text_input(
        "소재 검색",
        placeholder="소재명 또는 화학식 검색"
    )

    filtered = DATA.copy()

    if search:
        filtered = filtered[
            filtered["소재"].str.contains(search, case=False)
            | filtered["화학식"].str.contains(search, case=False)
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("MATERIAL CHARACTERIZATION")

    selected = st.multiselect(
        "비교할 양극재 선택",
        DATA["소재"].tolist(),
        default=["LFP", "NCM811", "LMFP"]
    )

    if selected:
        comparison = DATA[DATA["소재"].isin(selected)]

        metric = st.selectbox(
            "분석 특성",
            list(CRITERIA.keys())
        )

        fig = px.bar(
            comparison,
            x="소재",
            y=metric,
            color="소재",
            title=f"{metric} 특성 비교"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#102337",
            font_color="#e6f3fa"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("MULTI-PROPERTY RADAR")
        st.plotly_chart(
            radar_chart(DATA, selected),
            use_container_width=True
        )

    if st.button("소재 분석 연구 완료"):
        if award_xp("materials", 25):
            st.success("소재 분석 완료: 25 XP 획득")
        else:
            st.info("이미 완료한 연구입니다.")


# =========================================================
# ROOM 3 : BATTERY TESTING LAB
# =========================================================

elif room == "배터리 실험실":

    page_header(
        "FACILITY 02 / BATTERY TESTING",
        "배터리 실험실",
        "실험 조건을 설정하고 교육용 계산 모델을 실행합니다."
    )

    st.markdown(
        '<div class="notice">이 실험은 실제 배터리의 전기화학 반응이나 '
        '열화를 재현하지 않는 단순 교육용 시뮬레이션입니다. '
        '결과는 실제 용량 유지율이나 수명 예측값이 아닙니다.</div>',
        unsafe_allow_html=True
    )

    st.subheader("EXPERIMENT CONFIGURATION")

    with st.container(border=True):
        material = st.selectbox(
            "시험 대상 양극재",
            DATA["소재"].tolist()
        )

        col1, col2 = st.columns(2)

        with col1:
            temperature = st.slider(
                "설정 온도 (℃)",
                0, 60, 25
            )

        with col2:
            rate = st.select_slider(
                "충전 속도 (C-rate)",
                options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                value=1.0
            )

        cycle = st.slider(
            "가상 충·방전 횟수",
            100, 3000, 1000, 100
        )

    if st.button("실험 장비 가동 / RUN EXPERIMENT"):

        row = DATA[DATA["소재"] == material].iloc[0]

        temperature_factor = max(
            0.55, 1 - abs(temperature - 25) * 0.006
        )
        rate_factor = max(
            0.5, 1 - max(0, rate - 1) * 0.12
        )
        cycle_factor = max(
            0.5, 1 - cycle / row["수명"] * 0.35
        )

        index = (
            temperature_factor
            * rate_factor
            * cycle_factor
            * 100
        )

        result = {
            "소재": material,
            "온도": temperature,
            "충전 속도": rate,
            "가상 사이클": cycle,
            "교육용 지수": round(index, 2)
        }

        st.session_state.latest_experiment = result
        st.session_state.experiment_count += 1

        award_xp("experiment", 30)

    if st.session_state.latest_experiment:
        result = st.session_state.latest_experiment

        st.divider()
        st.subheader("EXPERIMENT RESULT")

        a, b, c = st.columns(3)
        a.metric("온도", f"{result['온도']} ℃")
        b.metric("충전 속도", f"{result['충전 속도']} C")
        c.metric("교육용 지수", f"{result['교육용 지수']}")

        st.write(
            f"선택 소재: **{result['소재']}**"
        )
        st.write(
            f"설정한 가상 충·방전 횟수: **{result['가상 사이클']}회**"
        )
        st.info(
            "이 지수는 설정한 변수에 따라 변화하는 교육용 계산 결과입니다. "
            "실제 소재별 열화 특성을 반영하지 않습니다."
        )


# =========================================================
# ROOM 4 : AI ANALYSIS CENTER
# =========================================================

elif room == "AI 분석 센터":

    page_header(
        "FACILITY 03 / COMPUTATIONAL MATERIALS SCIENCE",
        "AI 분석 센터",
        "다기준 최적화, 파레토 분석 및 민감도 분석을 수행합니다."
    )

    tab1, tab2, tab3 = st.tabs([
        "소재 최적화",
        "파레토 분석",
        "민감도 분석"
    ])

    # -------- OPTIMIZATION --------

    with tab1:

        st.subheader("MULTI-CRITERIA OPTIMIZATION")

        scenarios = {
            "전기자동차(EV)": {
                "에너지밀도": 5,
                "수명": 3,
                "안전성": 4,
                "원가": 2,
                "출력특성": 4,
                "자원안정성": 2
            },
            "에너지저장장치(ESS)": {
                "에너지밀도": 2,
                "수명": 5,
                "안전성": 5,
                "원가": 4,
                "출력특성": 2,
                "자원안정성": 4
            },
            "휴대용 전자기기": {
                "에너지밀도": 5,
                "수명": 2,
                "안전성": 3,
                "원가": 2,
                "출력특성": 3,
                "자원안정성": 2
            }
        }

        scenario = st.selectbox(
            "사용 목적",
            list(scenarios.keys())
        )

        weights = {}
        weight_cols = st.columns(3)

        for i, criterion in enumerate(CRITERIA):
            with weight_cols[i % 3]:
                weights[criterion] = st.slider(
                    criterion,
                    0, 5,
                    scenarios[scenario][criterion],
                    key=f"opt_{criterion}"
                )

        if sum(weights.values()) == 0:
            st.error("하나 이상의 가중치를 설정해야 합니다.")
        else:
            ranking = optimize_materials(DATA, weights)
            st.dataframe(
                ranking,
                use_container_width=True,
                hide_index=True
            )

            fig = px.bar(
                ranking.sort_values("종합점수"),
                x="종합점수",
                y="소재",
                orientation="h",
                color="종합점수",
                title="가중치 기반 소재 평가"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#102337",
                font_color="#e6f3fa"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.success(
                f"현재 설정의 1위 후보: {ranking.iloc[0]['소재']}"
            )

            st.caption(
                "순위는 현재 데이터와 사용자가 설정한 가중치에 종속됩니다."
            )

            if st.button("최적화 분석 기록"):
                st.session_state.latest_ranking = ranking
                if award_xp("optimization", 30):
                    st.success("분석 기록 완료: 30 XP 획득")
                else:
                    st.info("이미 완료한 연구입니다.")

    # -------- PARETO --------

    with tab2:

        st.subheader("PARETO FRONTIER ANALYSIS")

        pareto = pareto_analysis(DATA)
        st.session_state.latest_pareto = pareto

        st.dataframe(
            pareto,
            use_container_width=True,
            hide_index=True
        )

        normalized = normalize_data(DATA)

        fig = px.scatter(
            x=normalized["에너지밀도"],
            y=normalized["안전성"],
            text=DATA["소재"],
            color=pareto["파레토 최적 후보"].map({
                True: "파레토 최적 후보",
                False: "열위 후보"
            }),
            title="에너지밀도와 안전성의 관계",
            labels={
                "x": "에너지밀도 정규화값",
                "y": "안전성 정규화값",
                "color": "분류"
            }
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#102337",
            font_color="#e6f3fa"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "파레토 최적 후보는 모든 평가 기준에서 절대적으로 가장 좋은 "
            "소재라는 뜻이 아닙니다. 다른 후보에 의해 모든 기준에서 "
            "동시에 뒤처지지 않는 후보를 뜻합니다."
        )

        if st.button("파레토 분석 기록"):
            if award_xp("pareto", 30):
                st.success("분석 기록 완료: 30 XP 획득")
            else:
                st.info("이미 완료한 연구입니다.")

    # -------- SENSITIVITY --------

    with tab3:

        st.subheader("WEIGHT SENSITIVITY ANALYSIS")

        criterion = st.selectbox(
            "변화시킬 기준",
            list(CRITERIA.keys()),
            key="sensitivity_criterion"
        )

        base = st.slider(
            "기준 가중치",
            1, 5, 3,
            key="sensitivity_base"
        )

        base_weights = {
            key: 3 for key in CRITERIA
        }
        base_weights[criterion] = base

        sensitivity = make_sensitivity(
            DATA, criterion, base_weights
        )
        st.session_state.latest_sensitivity = sensitivity

        st.dataframe(
            sensitivity,
            use_container_width=True,
            hide_index=True
        )

        fig = px.line(
            sensitivity,
            x="가중치 변화",
            y="순위",
            color="소재",
            markers=True,
            title=f"{criterion} 가중치 변화에 따른 순위 변동"
        )
        fig.update_yaxes(autorange="reversed", dtick=1)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#102337",
            font_color="#e6f3fa"
        )
        st.plotly_chart(fig, use_container_width=True)

        if st.button("민감도 분석 기록"):
            if award_xp("sensitivity", 30):
                st.success("분석 기록 완료: 30 XP 획득")
            else:
                st.info("이미 완료한 연구입니다.")


# =========================================================
# ROOM 5 : RESEARCH ARCHIVE
# =========================================================

elif room == "연구 기록 보관소":

    page_header(
        "FACILITY 04 / RESEARCH ARCHIVE",
        "연구 기록 보관소",
        "연구 활동, 실험 결과 및 분석 보고서를 관리합니다."
    )

    st.subheader("RESEARCH LOG")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("현재 저장된 연구 활동이 없습니다.")

    st.divider()

    st.subheader("LATEST EXPERIMENT")

    if st.session_state.latest_experiment:
        st.json(st.session_state.latest_experiment)
    else:
        st.caption("실험 기록이 없습니다.")

    st.subheader("LATEST OPTIMIZATION")

    if st.session_state.latest_ranking is not None:
        st.dataframe(
            st.session_state.latest_ranking,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("최적화 분석 기록이 없습니다.")

    st.subheader("RESEARCH REPORT")

    report = f"""
CAMO - CATHODE ADVANCED MATERIAL OPTIMIZER
RESEARCH REPORT

작성 시각: {datetime.now().strftime("%Y-%m-%d %H:%M")}

1. 연구 주제
이차전지 양극재의 특성 비교 및 다기준 최적화

2. 연구 목적
양극재의 에너지밀도, 수명, 안전성, 원가,
출력특성 및 자원안정성을 비교하고
사용 목적에 적합한 후보를 탐색한다.

3. 연구 활동
{pd.DataFrame(st.session_state.history).to_string(index=False)
 if st.session_state.history else "기록 없음"}

4. 최근 실험 결과
{st.session_state.latest_experiment
 if st.session_state.latest_experiment else "실험 기록 없음"}

5. 최적화 결과
{st.session_state.latest_ranking.to_string(index=False)
 if st.session_state.latest_ranking is not None else "분석 기록 없음"}

6. 데이터 및 모델의 한계
기본 데이터는 교육용 예시값이다.
가상 실험은 실제 전지의 전기화학적 성능을 예측하지 않는다.
최적화 결과는 데이터와 가중치 설정에 따라 달라진다.
실제 연구 활용 전에는 검증된 문헌 데이터와
측정 조건을 확보해야 한다.
"""

    st.download_button(
        "연구 보고서 다운로드",
        data=report,
        file_name="CAMO_research_report.txt",
        mime="text/plain"
    )

    st.download_button(
        "양극재 데이터 CSV 다운로드",
        data=DATA.to_csv(index=False).encode("utf-8-sig"),
        file_name="CAMO_material_database.csv",
        mime="text/csv"
    )

    st.download_button(
        "연구 이력 CSV 다운로드",
        data=pd.DataFrame(
            st.session_state.history
        ).to_csv(index=False).encode("utf-8-sig"),
        file_name="CAMO_research_history.csv",
        mime="text/csv"
    )


# -------------------- FOOTER --------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#7897aa;font-size:11px;">
    CAMO RESEARCH INSTITUTE · CATHODE MATERIAL OPTIMIZATION SYSTEM<br>
    EDUCATIONAL SIMULATION · VERSION 2.0
    </div>
    """,
    unsafe_allow_html=True
)
