import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Try importing seaborn safely
try:
    import seaborn as sns
    seaborn_available = True
except ImportError:
    seaborn_available = False
    st.warning("⚠️ Seaborn is not installed. Using Matplotlib fallback mode.")

# =======================================================
# PAGE CONFIGURATION
# =======================================================
st.set_page_config(page_title="Student Academic Visualization Report", layout="wide")

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
# HELPER FUNCTION (UNIVERSAL PLOTTING)
# =======================================================
def plot_chart(kind, data, x=None, y=None, hue=None, title=None):
    """Helper function to plot with Seaborn or Matplotlib fallback."""
    fig, ax = plt.subplots(figsize=(8, 5))
    if seaborn_available:
        import seaborn as sns
        sns.set(style="whitegrid", palette="Set2")
        if kind == "box":
            sns.boxplot(x=x, y=y, data=data, ax=ax)
        elif kind == "violin":
            sns.violinplot(x=x, y=y, data=data, inner='quartile', ax=ax)
        elif kind == "bar":
            sns.barplot(x=x, y=y, data=data, ci=None, ax=ax)
        elif kind == "scatter":
            sns.scatterplot(x=x, y=y, hue=hue, data=data, s=80, ax=ax)
        elif kind == "heatmap":
            sns.heatmap(data, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        elif kind == "line":
            sns.lineplot(x=x, y=y, data=data, marker='o', ci=None, ax=ax)
    else:
        if kind == "box":
            data.boxplot(column=y, by=x, ax=ax)
        elif kind == "bar":
            data.groupby(x)[y].mean().plot(kind='bar', ax=ax)
        elif kind == "scatter":
            ax.scatter(data[x], data[y], alpha=0.6)
        elif kind == "line":
            data.groupby(x)[y].mean().plot(kind='line', marker='o', ax=ax)
        elif kind == "heatmap":
            cax = ax.matshow(data.corr(), cmap='coolwarm')
            fig.colorbar(cax)
    if title:
        ax.set_title(title)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =======================================================
# PAGE 1: DATASET SELECTION & RELEVANCE
# =======================================================
if page == "Dataset Selection & Relevance":
    st.title("🎓 Dataset Selection & Relevance")

    st.markdown("""
    **Dataset Title:** Student Academic and Behavioral Research Information  
    **Source:** Internal dataset (ResearchInformation3.csv)  
    **Type:** Structured CSV file  
    **Scope:** Student records with gender, department, attendance, income, grades, and extracurricular data.
    """)

    st.markdown("""
    ### 🧩 Relevance & Justification
    This dataset is ideal for exploring **academic success patterns** across multiple variables:
    - Academic trends by gender and department  
    - Effects of socioeconomic factors on performance  
    - Skills and extracurricular engagement impact
    """)

    st.dataframe(df.head(), use_container_width=True)
    st.info(f"Total Records: {df.shape[0]} | Columns: {df.shape[1]} | Missing Values: {df.isnull().sum().sum()}")

# =======================================================
# PAGE 2: ACADEMIC PERFORMANCE TRENDS
# =======================================================
elif page == "Page 1 – Academic Performance Trends":
    st.title("🎯 Objective 1: Academic Performance Trends")
    st.info("Objective: Examine variations in academic performance across departments, gender, and attendance.")

    st.markdown("""
    ### 🧾 Summary Box
    Higher attendance and consistent departmental results correlate with better GPA outcomes.
    Gender differences are minimal, but attendance strongly predicts GPA stability.
    """)

    plot_chart("box", df, x='Department', y='Overall', title="GPA Distribution by Department")
    plot_chart("violin", df, x='Gender', y='Overall', title="GPA by Gender")
    plot_chart("bar", df, x='Attendance', y='Overall', title="Average GPA by Attendance")

    st.markdown("""
    **Interpretation:**  
    - Departments with balanced assessment systems show stable GPA ranges.  
    - Gender influence is minor; attendance is the strongest GPA predictor.
    """)

# =======================================================
# PAGE 3: SOCIOECONOMIC & LIFESTYLE FACTORS
# =======================================================
elif page == "Page 2 – Socioeconomic & Lifestyle Factors":
    st.title("💰 Objective 2: Socioeconomic and Lifestyle Factors")
    st.info("Objective: Explore how income, hometown, and gaming habits influence GPA.")

    st.markdown("""
    ### 🧾 Summary Box
    Students from higher-income families and city regions perform better academically.
    Longer gaming hours are linked to lower GPAs.
    """)

    plot_chart("bar", df, x='Income', y='Overall', title="Average GPA by Income")
    plot_chart("scatter", df, x='Gaming', y='Overall', title="Gaming Time vs GPA")
    corr = df[['HSC', 'SSC', 'Computer', 'English', 'Last', 'Overall']].corr()
    plot_chart("heatmap", corr, title="Correlation Heatmap")

    st.markdown("""
    **Interpretation:**  
    - Income positively influences GPA via better access to learning resources.  
    - Excessive gaming time reduces focus and GPA.  
    - English and Computer subjects strongly correlate with Overall performance.
    """)

# =======================================================
# PAGE 4: SKILLS & EXTRACURRICULAR IMPACT
# =======================================================
elif page == "Page 3 – Skills & Extracurricular Impact":
    st.title("🧠 Objective 3: Skills and Extracurricular Impact")
    st.info("Objective: Assess how computer literacy, English proficiency, and extracurricular participation affect GPA.")

    st.markdown("""
    ### 🧾 Summary Box
    Students with strong computer and English skills achieve higher GPAs.  
    Extracurricular participation fosters balanced and improved performance.
    """)

    plot_chart("scatter", df, x='Computer', y='Overall', hue='Extra', title="Computer Skills vs GPA by Extracurriculars")
    plot_chart("line", df, x='English', y='Overall', title="Average GPA by English Proficiency")
    plot_chart("bar", df, x='Extra', y='Overall', title="Average GPA by Extracurricular Involvement")

    st.markdown("""
    **Interpretation:**  
    - High skill levels in English and Computer Science boost GPA consistency.  
    - Students active in extracurriculars demonstrate well-rounded academic outcomes.
    """)

# =======================================================
# FOOTER
# =======================================================
st.sidebar.markdown("---")
st.sidebar.caption("Developed for Scientific Visualization Assignment © 2025")
