import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------
# Streamlit Page Setup
# --------------------------------------------
st.set_page_config(page_title="Student Academic Visualization Dashboard", layout="wide")

st.title("Student Academic Visualization Dashboard")

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
st.sidebar.header("Menu")
    "Academic Performance Trends", 
    "Socioeconomic & Lifestyle Factors",
    "Skills & Extracurricular Impact"
])

# --------------------------------------------
# Objective 1: Academic Performance Trends
# --------------------------------------------
if page == "Academic Performance Trends":
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

    # 2️⃣ Violin Plot – GPA by Gender
    fig2 = px.violin(
        df, x='Gender', y='Overall', color='Gender',
        box=True, points='all', title="Overall GPA by Gender"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- 3️⃣ Pie Chart – Average GPA by Attendance ---
    avg_attendance = df.groupby('Attendance')['Overall'].mean().reset_index()
    fig3 = px.pie(
        avg_attendance,
        values='Overall',
        names='Attendance',
        title="Average GPA by Attendance Level",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    fig3.update_traces(
        textinfo='percent+label',
        pull=[0.05]*len(avg_attendance),
        textfont_size=14
    )
    fig3.update_layout(
        font=dict(size=14)
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    - The boxplot shows that some departments maintain more consistent GPA ranges.  
    - The histogram indicates GPA distribution is similar across genders.  
    - The **pie chart** highlights that students with **high attendance** contribute the most to strong GPA performance,  
      reaffirming attendance as a key factor in academic success.
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

    # 7️⃣ Density Plot – Computer Skill vs GPA
    import plotly.express as px

    # Clean data to ensure numeric columns only
    df_density = df[['Computer', 'Overall']].dropna()
    df_density = df_density[df_density['Computer'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]
    df_density = df_density.astype({'Computer': float, 'Overall': float})

    # Create density contour plot
    fig7 = px.density_contour(
        df_density,
        x='Computer',
        y='Overall',
        title="Density Plot of Computer Skill vs GPA"
    )

    # Fill the contour for better readability
    fig7.update_traces(contours_coloring="fill", contours_showlines=False)
    fig7.update_layout(
        xaxis_title="Computer Skill Level",
        yaxis_title="GPA",
        plot_bgcolor="white",
        font=dict(size=14)
    )

    st.plotly_chart(fig7, use_container_width=True)

    # 8️⃣ Line Chart – GPA by English Proficiency
    avg_english = df.groupby('English', as_index=False)['Overall'].mean()
    fig8 = px.line(
        avg_english, x='English', y='Overall', markers=True,
        title="Average GPA by English Proficiency"
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 9️⃣Strip Plot – GPA by Extracurricular Involvement
    import plotly.express as px

    fig9 = px.strip(
        df,
        x='Extra',
        y='Overall',
        title="GPA by Extracurricular Involvement",
        stripmode='overlay',
    )
    fig9.update_traces(jitter=0.35, opacity=0.7)
    fig9.update_layout(
        xaxis_title="Extracurricular Involvement",
        yaxis_title="GPA",
        plot_bgcolor="white",
        font=dict(size=14)
    )
    st.plotly_chart(fig9, use_container_width=True)

# --------------------------------------------
st.markdown("---")
st.caption("Developed for Scientific Visualization Assignment © 2025")
