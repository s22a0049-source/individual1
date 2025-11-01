import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Student Academic Visualization Report", layout="wide")

# Load dataset
df = pd.read_csv("ResearchInformation3.csv")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Dataset Overview",
    "Page 1 – Academic Performance Trends",
    "Page 2 – Socioeconomic & Lifestyle Factors",
    "Page 3 – Skills & Extracurricular Impact"
])

# Apply consistent theme
sns.set(style="whitegrid", palette="pastel")

# =======================================================
# PAGE 0: DATASET OVERVIEW
# =======================================================
if page == "Dataset Overview":
    st.title("🎓 Student Academic Visualization Report")
    st.markdown("""
    This dashboard explores how **academic performance** is influenced by
    various **socioeconomic, lifestyle, and skill-related factors** among students.
    """)
    
    st.subheader("📘 Dataset Overview")
    st.write(df.head())

    st.markdown("**Dataset Summary:**")
    st.write(df.describe(include='all'))

    st.info(f"Total Records: {df.shape[0]} | Columns: {df.shape[1]} | Missing Values: {df.isnull().sum().sum()}")

# =======================================================
# PAGE 1: Academic Performance Trends
# =======================================================
elif page == "Page 1 – Academic Performance Trends":
    st.header("🎯 Objective 1: Academic Performance Trends")
    st.markdown("""
    **Objective:** Analyze variations in academic performance across departments, gender, and attendance levels.
    
    **Key Insight:** Higher attendance and consistent departmental performance contribute positively to overall GPA.
    """)

    # 1. Boxplot – GPA by Department
    st.subheader("Overall GPA Distribution by Department")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x='Department', y='Overall', data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 2. Violin Plot – GPA by Gender
    st.subheader("Overall GPA by Gender")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.violinplot(x='Gender', y='Overall', data=df, inner='box', ax=ax)
    st.pyplot(fig)

    # 3. Bar Chart – GPA by Attendance
    st.subheader("Average GPA by Attendance Level")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.barplot(x='Attendance', y='Overall', data=df, estimator='mean', ci=None, ax=ax)
    st.pyplot(fig)

# =======================================================
# PAGE 2: Socioeconomic & Lifestyle Factors
# =======================================================
elif page == "Page 2 – Socioeconomic & Lifestyle Factors":
    st.header("💰 Objective 2: Socioeconomic and Lifestyle Factors")
    st.markdown("""
    **Objective:** Explore how income, hometown, and gaming habits influence academic performance.
    
    **Key Insight:** Students from higher income families and cities show higher GPAs, while heavy gaming time is linked to lower performance.
    """)

    # 4. Bar Chart – Average GPA by Income
    st.subheader("Average GPA by Family Income")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x='Income', y='Overall', data=df, estimator='mean', ci=None, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 5. Scatter Plot – Gaming Time vs GPA
    st.subheader("Gaming Time vs GPA")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.stripplot(x='Gaming', y='Overall', data=df, jitter=True, ax=ax)
    st.pyplot(fig)

    # 6. Heatmap – Correlation between academic metrics
    st.subheader("Correlation Heatmap (HSC, SSC, Computer, English, GPA)")
    fig, ax = plt.subplots(figsize=(6,4))
    corr = df[['HSC', 'SSC', 'Computer', 'English', 'Last', 'Overall']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)

# =======================================================
# PAGE 3: Skills & Extracurricular Impact
# =======================================================
elif page == "Page 3 – Skills & Extracurricular Impact":
    st.header("🧠 Objective 3: Skills and Extracurricular Impact")
    st.markdown("""
    **Objective:** Assess how computer literacy, English proficiency, and extracurricular participation affect student outcomes.
    
    **Key Insight:** Students with strong technical/language skills and active extracurricular participation tend to perform better academically.
    """)

    # 7. Scatter Plot – Computer Skills vs GPA (colored by Extra)
    st.subheader("Computer Skills vs GPA (by Extracurricular Involvement)")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.scatterplot(x='Computer', y='Overall', hue='Extra', data=df, s=80, ax=ax)
    st.pyplot(fig)

    # 8. Line Chart – Average GPA by English Proficiency
    st.subheader("Average GPA by English Proficiency Level")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.lineplot(x='English', y='Overall', data=df, estimator='mean', ci=None, marker='o', ax=ax)
    st.pyplot(fig)

    # 9. Grouped Bar Chart – GPA by Extracurricular Participation
    st.subheader("Average GPA by Extracurricular Participation")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.barplot(x='Extra', y='Overall', data=df, estimator='mean', ci=None, ax=ax)
    st.pyplot(fig)

# =======================================================
# FOOTER
# =======================================================
st.sidebar.markdown("---")
st.sidebar.info("Developed for Scientific Visualization Assignment\n© 2025 Student Performance Analysis")

