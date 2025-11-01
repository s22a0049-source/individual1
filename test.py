import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------
# Streamlit Page Setup
# --------------------------------------------
st.set_page_config(page_title="Student Academic Visualization Dashboard", layout="wide")

st.title("Student Academic Visualization Dashboard")

st.markdown("""
Explore the student dataset through **interactive scientific visualizations**.
Each section focuses on one objective to uncover meaningful academic insights.
""")

# --------------------------------------------
# Load Dataset
# --------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ResearchInformation3.csv")

df = load_data()

# --------------------------------------------
# Sidebar Navigation
# --------------------------------------------
st.sidebar.header("📄 Visualization Pages")
page = st.sidebar.radio("Select Analysis Section", [
    "Dataset Selection & Relevance",
    "Academic Performance Trends",
    "Socioeconomic & Lifestyle Factors",
    "Skills & Extracurricular Impact"
])

# --------------------------------------------
# Dataset Selection & Relevance
# --------------------------------------------
if page == "Dataset Selection & Relevance":
    st.header("Dataset Selection & Relevance")

    st.markdown("""
    **Dataset Title:** Research Information on Student Academic and Behavioral Factors  
    **Source:** Collected dataset (inspired by Mendeley Data)  
    **Type:** Structured CSV containing academic, behavioral, and demographic attributes  
    """)

    st.markdown("""
    ### Relevance
    This dataset explores **academic performance**, **socioeconomic status**, and **skills**.
    It supports visualization-based analysis of student success factors.
    """)

    st.dataframe(df.head(), use_container_width=True)
    st.info(f"Total Records: {df.shape[0]} | Columns: {df.shape[1]} | Missing Values: {df.isnull().sum().sum()}")

# --------------------------------------------
# Objective 1: Academic Performance Trends
# --------------------------------------------
elif page == "Academic Performance Trends":
    st.header("Objective 1: Academic Performance Trends")
    st.subheader("Objective Statement")
    st.write("Analyze GPA variation by department, gender, and attendance level.")

    st.success("""
    **Summary Box:**  
    Higher attendance leads to higher GPA stability.  
    Department-wise performance varies slightly, and gender impact is minimal.
    """)

    # --- 1️⃣ Boxplot – Overall GPA by Department ---
    fig1 = px.box(
        df,
        x='Department',
        y='Overall',
        color='Department',
        title="Overall GPA Distribution by Department"
    )
    fig1.update_layout(
        xaxis_title="Department",
        yaxis_title="Overall GPA",
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- 2️⃣ Histogram – GPA Distribution by Gender ---
    fig2 = px.histogram(
        df,
        x='Overall',
        color='Gender',
        barmode='overlay',
        opacity=0.7,
        nbins=20,
        title="GPA Frequency Distribution by Gender"
    )
    fig2.update_layout(
        xaxis_title="Overall GPA",
        yaxis_title="Number of Students",
        bargap=0.1
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- 3️⃣ Bar Chart – Average GPA by Attendance ---
    fig3 = px.bar(
        df.groupby('Attendance')['Overall'].mean().reset_index(),
        x='Attendance',
        y='Overall',
        title="Average GPA by Attendance Level",
        text_auto=True
    )
    fig3.update_layout(
        xaxis_title="Attendance Level",
        yaxis_title="Average GPA"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    - Departments show varied GPA levels, indicating different grading or performance patterns.  
    - The histogram shows a balanced GPA distribution between genders, with only minor variation.  
    - Attendance remains the strongest and most consistent factor influencing GPA outcomes.
    """)


# --------------------------------------------
# Objective 2: Socioeconomic & Lifestyle Factors
# --------------------------------------------
elif page == "Socioeconomic & Lifestyle Factors":
    st.header("Objective 2: Socioeconomic & Lifestyle Factors")
    st.subheader("Objective Statement")
    st.write("Investigate how income and gaming habits influence academic performance.")

    st.success("""
    **Summary Box:**  
    Higher income correlates with better GPA due to access to resources.  
    Extended gaming hours tend to lower performance levels.
    """)

    # 4️⃣ Bar Chart – Average GPA by Income Level
    avg_income = df.groupby('Income', as_index=False)['Overall'].mean()
    fig4 = px.bar(
        avg_income, x='Income', y='Overall', color='Income', text='Overall',
        title="Average GPA by Income Level"
    )
    fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig4.update_layout(yaxis_title="Average GPA", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ Scatter Plot – Gaming Duration vs GPA
    fig5 = px.scatter(
        df, x='Gaming', y='Overall', color='Gender', size='Overall',
        title="Gaming Duration vs GPA", hover_data=['Department']
    )
    st.plotly_chart(fig5, use_container_width=True)

    # 6️⃣ Heatmap – Correlation Matrix
    corr = df[['HSC', 'SSC', 'Computer', 'English', 'Last', 'Overall']].corr().round(2)
    fig6 = px.imshow(
        corr, text_auto=True, color_continuous_scale='RdBu_r',
        title="Correlation Heatmap of Academic Variables"
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Income and time management significantly influence GPA outcomes.
    """)

# --------------------------------------------
# Objective 3: Skills & Extracurricular Impact
# --------------------------------------------
elif page == "Skills & Extracurricular Impact":
    st.header("Objective 3: Skills & Extracurricular Impact")
    st.subheader("Objective Statement")
    st.write("Assess how English proficiency, computer skills, and extracurricular activities influence GPA.")

    st.success("""
    **Summary Box:**  
    Strong language and technical skills support higher GPA.  
    Students active in extracurriculars maintain balanced academic performance.
    """)

    # 7️⃣ Grouped Bar Chart – GPA by Computer Skill & Extracurriculars
    avg_skill_extra = df.groupby(['Computer', 'Extra'], as_index=False)['Overall'].mean()
    fig7 = px.bar(
        avg_skill_extra, x='Computer', y='Overall', color='Extra',
        barmode='group', text='Overall',
        title="Average GPA by Computer Skill and Extracurricular Participation"
    )
    fig7.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig7.update_layout(yaxis_title="Average GPA")
    st.plotly_chart(fig7, use_container_width=True)

    # 8️⃣ Line Chart – GPA by English Proficiency
    avg_english = df.groupby('English', as_index=False)['Overall'].mean()
    fig8 = px.line(
        avg_english, x='English', y='Overall', markers=True,
        title="Average GPA by English Proficiency"
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 9️⃣ Bar Chart – GPA by Extracurricular Involvement
    avg_extra = df.groupby('Extra', as_index=False)['Overall'].mean()
    fig9 = px.bar(
        avg_extra, x='Extra', y='Overall', color='Extra', text='Overall',
        title="Average GPA by Extracurricular Involvement"
    )
    fig9.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig9.update_layout(yaxis_title="Average GPA", showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Higher technical and language proficiency enhance academic success,
    while extracurricular involvement fosters balanced student development.
    """)

# --------------------------------------------
st.markdown("---")
st.caption("Developed for Scientific Visualization Assignment © 2025")
