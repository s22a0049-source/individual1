import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Try importing seaborn safely
try:
    import seaborn as sns
    seaborn_available = True
except ImportError:
    seaborn_available = False
    st.warning("⚠️ Seaborn not found — using Matplotlib fallback mode.")

st.title("📊 Student Academic Visualization Dashboard")

st.markdown("""
Explore the student dataset through **scientific visualization techniques**.
Each section focuses on one objective to uncover meaningful academic insights.
""")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("ResearchInformation3.csv")

df = load_data()

# Sidebar navigation within visualization page
st.sidebar.header("📄 Visualization Pages")
page = st.sidebar.radio("Select Analysis Section", [
    "📘 Dataset Selection & Relevance",
    "🎯 Academic Performance Trends",
    "💰 Socioeconomic & Lifestyle Factors",
    "🧠 Skills & Extracurricular Impact"
])

# Helper function for plotting
def plot_chart(kind, data, x=None, y=None, hue=None, title=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    if seaborn_available:
        sns.set(style="whitegrid", palette="pastel")
        if kind == "box":
            sns.boxplot(x=x, y=y, data=data, ax=ax)
        elif kind == "violin":
            sns.violinplot(x=x, y=y, data=data, inner='quartile', ax=ax)
        elif kind == "bar":
            sns.barplot(x=x, y=y, data=data, ci=None, ax=ax)
        elif kind == "grouped_bar":
            sns.barplot(x=x, y=y, hue=hue, data=data, ci=None, ax=ax)
        elif kind == "scatter":
            sns.scatterplot(x=x, y=y, hue=hue, data=data, s=80, ax=ax)
        elif kind == "heatmap":
            sns.heatmap(data, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        elif kind == "line":
            sns.lineplot(x=x, y=y, data=data, marker='o', ci=None, ax=ax)
    else:
        if kind == "bar":
            data.groupby(x)[y].mean().plot(kind='bar', ax=ax)
        elif kind == "grouped_bar":
            grouped = data.groupby([x, hue])[y].mean().unstack()
            grouped.plot(kind='bar', ax=ax)
        elif kind == "scatter":
            ax.scatter(data[x], data[y], alpha=0.6)
        elif kind == "line":
            data.groupby(x)[y].mean().plot(kind='line', marker='o', ax=ax)
        elif kind == "heatmap":
            cax = ax.matshow(data.corr(), cmap='coolwarm')
            fig.colorbar(cax)
    ax.set_title(title)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --------------------- Visualization Pages ---------------------

if page == "📘 Dataset Selection & Relevance":
    st.header("📘 Dataset Selection & Relevance")

    st.markdown("""
    **Dataset Title:** Research Information on Student Academic and Behavioral Factors  
    **Source:** Collected research dataset (`ResearchInformation3.csv`)  
    **Type:** Structured CSV — includes academic, behavioral, and demographic data.  
    """)

    st.markdown("""
    ### 🧩 Relevance
    This dataset enables exploration of **academic trends**, **socioeconomic influences**,  
    and **skills impact**, making it ideal for a scientific visualization study.
    """)

    st.dataframe(df.head(), use_container_width=True)
    st.info(f"Total Records: {df.shape[0]} | Columns: {df.shape[1]} | Missing Values: {df.isnull().sum().sum()}")

elif page == "🎯 Academic Performance Trends":
    st.header("🎯 Objective 1: Academic Performance Trends")
    st.subheader("Objective Statement")
    st.write("Analyze GPA variation by department, gender, and attendance level.")

    st.success("""
    **Summary Box:**  
    Higher attendance leads to higher GPA stability.  
    Department-wise performance varies slightly, and gender impact is minimal.
    """)

    plot_chart("box", df, x='Department', y='Overall', title="GPA Distribution by Department")
    plot_chart("violin", df, x='Gender', y='Overall', title="GPA by Gender")
    plot_chart("bar", df, x='Attendance', y='Overall', title="Average GPA by Attendance")

    st.markdown("""
    **Interpretation:** Departments show varied GPA levels, with attendance being the strongest performance indicator.
    """)

elif page == "💰 Socioeconomic & Lifestyle Factors":
    st.header("💰 Objective 2: Socioeconomic & Lifestyle Factors")
    st.subheader("Objective Statement")
    st.write("Investigate how income and gaming habits influence academic performance.")

    st.success("""
    **Summary Box:**  
    Higher income correlates with better GPA due to access to resources.  
    Extended gaming hours tend to lower performance levels.
    """)

    plot_chart("bar", df, x='Income', y='Overall', title="Average GPA by Income Level")
    plot_chart("scatter", df, x='Gaming', y='Overall', title="Gaming Duration vs GPA")
    corr = df[['HSC', 'SSC', 'Computer', 'English', 'Last', 'Overall']].corr()
    plot_chart("heatmap", corr, title="Correlation Heatmap")

    st.markdown("""
    **Interpretation:**  
    Income and time management significantly influence GPA outcomes.
    """)

elif page == "🧠 Skills & Extracurricular Impact":
    st.header("🧠 Objective 3: Skills & Extracurricular Impact")
    st.subheader("Objective Statement")
    st.write("Assess how English proficiency, computer skills, and extracurricular activities influence GPA.")

    st.success("""
    **Summary Box:**  
    Strong language and technical skills support higher GPA.  
    Students active in extracurriculars maintain balanced academic performance.
    """)

    # ✅ Visualization #7 changed from scatter to grouped bar
    plot_chart("grouped_bar", df, x='Computer', y='Overall', hue='Extra', title="Average GPA by Computer Skill and Extracurriculars")
    plot_chart("line", df, x='English', y='Overall', title="Average GPA by English Proficiency")
    plot_chart("bar", df, x='Extra', y='Overall', title="Average GPA by Extracurricular Involvement")

    st.markdown("""
    **Interpretation:**  
    Students with higher computer skills generally show better GPA outcomes.  
    The grouped bar chart makes it easier to compare academic impact between extracurricular participants and non-participants.
    """)

st.markdown("---")
st.caption("Developed for Scientific Visualization Assignment © 2025")
