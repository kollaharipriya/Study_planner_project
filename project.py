
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Page title
st.title("📚 Smart Study Plan")
st.write("Create a simple study plan based on your subjects, exam dates and priorities.")

# Student details
name = st.text_input("Enter your name:")
hours = st.number_input("Available study hours per day", min_value=1, max_value=12, value=3)

# Number of subjects
num_subjects = st.number_input(
    "Number of subjects",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

# Subject details
for i in range(int(num_subjects)):
    st.subheader(f"Subject {i + 1}")

    subject_name = st.text_input(
        "Subject name",
        key=f"name{i}"
    )

    exam_date = st.date_input(
        "Exam date",
        key=f"date{i}"
    )

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"],
        key=f"priority{i}"
    )

    progress = st.slider(
        "Progress (%)",
        0,
        100,
        0,
        key=f"progress{i}"
    )

    subjects.append({
        "Subject": subject_name,
        "Exam Date": exam_date,
        "Priority": priority,
        "Progress": progress
    })


# Create study plan
if st.button("Generate Study Plan"):

    priority_value = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    df = pd.DataFrame(subjects)

    # Calculate days remaining
    today = pd.Timestamp.today().normalize()

    df["Days Left"] = (
        pd.to_datetime(df["Exam Date"]) - today
    ).dt.days

    # Convert priority into numbers
    df["Priority Score"] = df["Priority"].map(priority_value)

    # Calculate study hours
    total_score = df["Priority Score"].sum()

    df["Study Hours"] = (
        hours * df["Priority Score"] / total_score
    ).round(2)

    # Display result
    st.success(f"Study plan created for {name}!")

    st.subheader("📅 Your Study Plan")

    st.dataframe(df)

    # Progress graph
    st.subheader("📊 Subject Progress")

    fig, ax = plt.subplots()

    sns.barplot(
        data=df,
        x="Subject",
        y="Progress",
        ax=ax
    )

    ax.set_ylabel("Progress (%)")
    ax.set_xlabel("Subject")

    st.pyplot(fig)

    # Save data in SQLite
    engine = create_engine("sqlite:///study_plan.db")

    df.to_sql(
        "study_plan",
        engine,
        if_exists="replace",
        index=False
    )

    st.success("Study plan saved successfully!")
