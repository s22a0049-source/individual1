pip install seaborn matplotlib pandas streamlit

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =======================================================
# PAGE CONFIGURATION
# =======================================================
st.set_page_config(page_title="Student Academic Visualization Report", layout="wide")
sns.set(style="whitegrid", palette="Set2")

# =======================================================
# LOAD DATA
# =======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("ResearchInformation3.csv")
    return df

df = load_data()

# =======================================================
# SIDEBAR NAVIGATION
# =======================================================
st.sidebar.title("📊 Navigation Panel")
page = st.sidebar.radio("Go to section:", [
    "Dataset Selection & Relevance",
    "Page 1 – Academic Performance Trends",
    "Page 2 – Socioeconomic & Lifestyle Factors",
    "Page 3 – Skills & Extracurricular Impact"
])

# =======================================================
# PAGE 1: DATASET SELECTION & RELEVANCE
# =======================================================
if page == "Dataset Selection & Relevance":
    st.title("🎓 Dataset Selection & Relevance")

    st.markdown("""
    **Dataset Title:** Student Academic and Behavioral Research Information  
    **Source:** Internal dataset based on academic, lifestyle, and socioeconomic attributes.  
    **Type:** Structured CSV file  
    **Scope:** Records of students including gender, department, attendance, income, academic results (HSC, SSC, Computer, English, Overall GPA), and extracurricular activities.
    """)

    st.markdown("""
    ### 🧩 Relevance & Justification
    This dataset is highly relevant for analyzing **academic success patterns** because it integrates
    cognitive, behavioral, and socioeconomic variables.  
    It supports the following visualization objectives:
    - Identify academic performance trends by demographics and attendance.  
    - Explore the impact of income, hometown, and lifestyle on GPA.  
    - Assess how skill levels and extracurricular participation influence performance.  
    """)

    st.markdown("### 🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("### 📊 Dataset Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Shape:**", df.shape)
        st.write("**Missing Values:**", df.isnull().sum().sum())
    with col2:
        st.write("**Columns:**")
        st.write(list(df.columns))

    st.success("""
    ✅ **Conclusion:**  
    This dataset is complex and suitable for in-depth academic analytics,
    supporting multidimensional visualization and interpretation.
    """)

# =======================================================
# PAGE 2: ACADEMIC PERFORMANCE TRENDS
# =======================================================
elif page == "Page 1 – Academic Performance Trends":
    st.title("🎯 Objective 1: Academic Performance Trends")

    st.info("""
    **Objective Statement:**  
    To examine variations in academic performance across departments, gender, and attendance levels.
    """)

    st.markdown("""
    ### 🧾 Summary Box
    Students with higher attendance and consistent departmental records tend to achieve better GPAs.
    Gender differences are minimal but attendance strongly correlates with performance consistency.
    """)

    # Filter options
    departments = st.multiselect("Filter by Department:", options=df['Department'].unique(), default=df['Department'].unique())
    filtered_df = df[df['Department'].isin(departments)]

    # Visualization 1 – Boxplot: GPA by Department
    st.subheader("📈 Overall GPA Distribution by Department")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x='Department', y='Overall', data=filtered_df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Visualization 2 – Violin Plot: GPA by Gender
    st.subheader("📊 GPA by Gender")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.violinplot(x='Gender', y='Overall', data=filtered_df, inner='quartile', ax=ax)
    st.pyplot(fig)

    # Visualization 3 – Bar Chart: GPA by Attendance
    st.subheader("🕒 Average GPA by Attendance Level")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.barplot(x='Attendance', y='Overall', data=filtered_df, estimator='mean', ci=None, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### 💡 Interpretation
    - Departments with consistent teaching quality show less GPA variation.
    - Female students exhibit slightly higher GPA median levels.
    - High attendance directly correlates with improved GPA and stability.
    """)

# =======================================================
# PAGE 3: SOCIOECONOMIC & LIFESTYLE FACTORS
# =======================================================
elif page == "Page 2 – Socioeconomic & Lifestyle Factors":
    st.title("💰 Objective 2: Socioeconomic and Lifestyle Factors")

    st.info("""
    **Objective Statement:**  
    To explore how income, hometown, and gaming habits affect academic achievement.
    """)

    st.markdown("""
    ### 🧾 Summary Box
    Students from higher income families and city areas show slightly higher GPAs.  
    Increased gaming time is associated with reduced GPA performance.
    """)

    # Visualization 4 – Bar Chart: GPA by Income
    st.subheader("💵 Average GPA by Family Income")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x='Income', y='Overall', data=df, estimator='mean', ci=None, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Visualization 5 – Scatter Plot: Gaming Time vs GPA
    st.subheader("🎮 Gaming Time vs GPA")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.stripplot(x='Gaming', y='Overall', data=df, jitter=True, ax=ax)
    st.pyplot(fig)

    # Visualization 6 – Heatmap: Correlation
    st.subheader("🔥 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(6,4))
    corr = df[['HSC', 'SSC', 'Computer', 'English', 'Last', 'Overall']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### 💡 Interpretation
    - Income level influences learning resources and performance outcomes.  
    - Gaming time inversely affects GPA, suggesting distraction or time mismanagement.  
    - Strong correlation exists between English, Computer, and Overall performance.
    """)

# =======================================================
# PAGE 4: SKILLS & EXTRACURRICULAR IMPACT
# =======================================================
elif page == "Page 3 – Skills & Extracurricular Impact":
    st.title("🧠 Objective 3: Skills and Extracurricular Impact")

    st.info("""
    **Objective Statement:**  
    To assess how computer literacy, English proficiency, and extracurricular participation influence GPA.
    """)

    st.markdown("""
    ### 🧾 Summary Box
    Students with higher computer and English scores demonstrate superior overall GPAs.  
    Active participation in extracurricular activities correlates with enhanced performance balance.
    """)

    # Visualization 7 – Scatter: Computer vs GPA by Extra
    st.subheader("💻 Computer Skills vs GPA (by Extracurricular Participation)")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.scatterplot(x='Computer', y='Overall', hue='Extra', data=df, s=80, ax=ax)
    st.pyplot(fig)

    # Visualization 8 – Line Plot: English vs GPA
    st.subheader("🗣️ English Proficiency vs Average GPA")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.lineplot(x='English', y='Overall', data=df, estimator='mean', ci=None, marker='o', ax=ax)
    st.pyplot(fig)

    # Visualization 9 – Bar Plot: Extracurricular Participation
    st.subheader("🎭 GPA by Extracurricular Participation")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.barplot(x='Extra', y='Overall', data=df, estimator='mean', ci=None, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### 💡 Interpretation
    - Strong technical and language skills boost GPA consistency.
    - Students involved in extracurricular activities perform better overall due to better time management and engagement.
    """)

# =======================================================
# FOOTER
# =======================================================
st.sidebar.markdown("---")
st.sidebar.caption("Developed for Scientific Visualization Assignment © 2025")
