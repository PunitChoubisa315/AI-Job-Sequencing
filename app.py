import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from johnson import johnsons_rule, calculate_schedule
from ai_model import predict_job_score


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Job Sequencing",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------
# Custom UI
# -----------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.result-box {
    padding: 18px;
    border-radius: 10px;
    border: 2px solid #ddd;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# Title
# -----------------------------------

st.markdown(
    '<div class="main-title">🤖 AI-Based Job Sequencing Optimization System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Operations Research + Johnson\'s Rule + AI Workload Analysis</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.header("📌 Project Information")

    st.write("**Problem:** Job Sequencing")

    st.write("**Machines:** 2")

    st.write("**Optimization:** Johnson's Rule")

    st.write("**AI:** Workload Analysis")

    st.divider()

    st.info(
        "Johnson's Rule calculates the optimal job sequence. "
        "The AI model analyzes workload based on historical job data."
    )


# -----------------------------------
# Historical Data
# -----------------------------------

st.subheader("📚 Historical Job Data")

data = pd.read_csv("data.csv")

st.dataframe(
    data,
    width="stretch"
)


st.divider()


# -----------------------------------
# Job Input
# -----------------------------------

st.subheader("⚙️ Enter Job Processing Time")

number_of_jobs = st.number_input(
    "🔢 Number of Jobs",
    min_value=2,
    max_value=20,
    value=6,
    step=1
)


jobs = [
    f"J{i}"
    for i in range(1, int(number_of_jobs) + 1)
]


st.write(
    "Enter the processing time for Machine 1 and Machine 2 for each job:"
)


# -----------------------------------
# Input Table
# -----------------------------------

input_columns = st.columns(3)

with input_columns[0]:
    st.markdown("**Job**")

with input_columns[1]:
    st.markdown("**Machine 1 Time**")

with input_columns[2]:
    st.markdown("**Machine 2 Time**")


for job in jobs:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"### {job}")

    with col2:
        st.number_input(
            f"M1 - {job}",
            min_value=0.0,
            value=0.0,
            key=job + "_m1"
        )

    with col3:
        st.number_input(
            f"M2 - {job}",
            min_value=0.0,
            value=0.0,
            key=job + "_m2"
        )


st.divider()


# -----------------------------------
# Generate Button
# -----------------------------------

if st.button(
    "🚀 Generate Optimal Sequence",
    width="stretch"
):

    job_times = {}


    # Collect Input

    for job in jobs:

        job_times[job] = {

            "M1": st.session_state[job + "_m1"],

            "M2": st.session_state[job + "_m2"]

        }


    # -----------------------------------
    # Johnson's Rule
    # -----------------------------------

    optimal_sequence = johnsons_rule(
        job_times
    )


    st.success(
        "✅ Johnson's Rule Applied Successfully!"
    )


    # -----------------------------------
    # Optimal Sequence
    # -----------------------------------

    st.subheader("🎯 Optimal Job Sequence")

    sequence_text = " → ".join(
        optimal_sequence
    )

    st.markdown(
        f'<div class="result-box">{sequence_text}</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------
    # Schedule Calculation
    # -----------------------------------

    rows, minimum_time, machine_2_idle = calculate_schedule(
        optimal_sequence,
        job_times
    )


    # -----------------------------------
    # Timing Table
    # -----------------------------------

    st.subheader("📊 Job Timing Table")

    schedule_df = pd.DataFrame(rows)

    st.dataframe(
        schedule_df,
        width="stretch"
    )


    # -----------------------------------
    # Gantt Chart
    # -----------------------------------

    st.subheader("📈 Gantt Chart")

    fig, ax = plt.subplots()

    for row in rows:

        # Machine 1

        ax.barh(
            1,
            row["M1 Out"] - row["M1 In"],
            left=row["M1 In"],
            height=0.3
        )


        # Machine 2

        ax.barh(
            0,
            row["M2 Out"] - row["M2 In"],
            left=row["M2 In"],
            height=0.3
        )


        # Job labels

        ax.text(
            (row["M1 In"] + row["M1 Out"]) / 2,
            1,
            row["Job"],
            ha="center",
            va="center"
        )


        ax.text(
            (row["M2 In"] + row["M2 Out"]) / 2,
            0,
            row["Job"],
            ha="center",
            va="center"
        )


    ax.set_yticks([0, 1])

    ax.set_yticklabels([
        "Machine 2",
        "Machine 1"
    ])

    ax.set_xlabel("Time")

    ax.set_title(
        "Job Sequencing Gantt Chart"
    )

    st.pyplot(fig)


    # -----------------------------------
    # AI Analysis
    # -----------------------------------

    st.subheader("🤖 AI Workload Analysis")

    ai_rows = []


    for job in jobs:

        m1 = job_times[job]["M1"]

        m2 = job_times[job]["M2"]


        score = predict_job_score(
            m1,
            m2
        )


        ai_rows.append({

            "Job": job,

            "Machine 1": m1,

            "Machine 2": m2,

            "AI Score": score

        })


    ai_df = pd.DataFrame(
        ai_rows
    )


    st.dataframe(
        ai_df,
        width="stretch"
    )


    st.info(
        "🤖 The AI model analyzes processing workload "
        "based on historical job data. "
        "The optimal sequence is determined using Johnson's Rule."
    )


    # -----------------------------------
    # Final Metrics
    # -----------------------------------

    st.subheader("📌 Final Result")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Jobs",
            int(number_of_jobs)
        )


    with col2:

        st.metric(
            "Minimum Elapsed Time",
            f"{minimum_time:.2f}"
        )


    with col3:

        st.metric(
            "Machine 2 Idle Time",
            f"{machine_2_idle:.2f}"
        )


# -----------------------------------
# How System Works
# -----------------------------------

with st.expander("ℹ️ How does this system work?"):

    st.write("""
    Step 1: Historical job data is loaded.

    Step 2: The user enters the processing time for Machine 1 and Machine 2.

    Step 3: Johnson's Rule determines the optimal sequence of all jobs.

    Step 4: The start and finish times for each machine are calculated.

    Step 5: The complete schedule is displayed using a Gantt Chart.

    Step 6: The AI model analyzes workload based on historical data.

    Step 7: The final result displays the minimum elapsed time and Machine 2 idle time.
    """)


st.divider()


st.caption(
    "AI-Based Job Sequencing Optimization System | Operations Research Project"
)
# AI_Job_Sequencing
# streamlit run app.py 