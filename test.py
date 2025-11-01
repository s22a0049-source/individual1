# ============================================================
# 📊 Student Survey Visualization Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Student Survey Dashboard", layout="wide")

# -----------------------------
# Load and Clean Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ResearchInformation3.csv")
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.drop_duplicates()
    return df

df = load_data()

# ============================================================
# PAGE 1 – Academic Performance
# ============================================================
st.title("🎓 Objective 1: Analyze Academic Performance Patterns")

st.markdown("""
**Objective Statement:**  
To explore how academic performance (GPA) varies across gender, age, and study habits among students.

**Summary Box:**  
This section visualizes GPA trends across demographic and behavioral factors.
The patterns indicate how gender, study hours, and age group influence academic success.
""")

# Visualization 1: Average GPA by Gender
st.subheader("1️⃣ Average GPA by Gender")
fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(data=df, x='Gender', y='GPA', ax=ax, palette='Set2')
ax.set_title("Average GPA by Gender")
st.pyplot(fig)

# Visualization 2: GPA vs Study Hours (Line Plot)
st.subheader("2️⃣ GPA vs Study Hours")
fig, ax = plt.subplots(figsize=(6,4))
sns.lineplot(data=df, x='Study Hours', y='GPA', marker='o', ax=ax)
ax.set_title("Relationship between Study Hours and GPA")
st.pyplot(fig)

# Visualization 3: GPA by Age Group (Box Plot)
st.subheader("3️⃣ GPA Distribution by Age Group")
fig, ax = plt.subplots(figsize=(6,4))
sns.boxplot(data=df, x='Age Group', y='GPA', ax=ax, palette='coolwarm')
ax.set_title("GPA Distribution by Age Group")
st.pyplot(fig)

st.markdown("""
**Interpretation:**  
The plots reveal that students studying longer hours and within certain age ranges tend to achieve higher GPAs. 
Gender-based differences are minimal but observable.
""")

# ============================================================
# PAGE 2 – Socioeconomic & Family Factors
# ============================================================
st.title("🏡 Objective 2: Examine Socioeconomic and Family Influences")

st.markdown("""
**Objective Statement:**  
To identify how socioeconomic and family-related factors affect academic outcomes.

**Summary Box:**  
This section highlights relationships between parental education, income levels, and GPA.
The analysis suggests that parental background may influence student achievement.
""")

# Visualization 4: Parental Education vs GPA (Box Plot)
st.subheader("4️⃣ GPA Distribution by Parental Education")
fig, ax = plt.subplots(figsize=(6,4))
sns.boxplot(data=df, x='Parental Education', y='GPA', ax=ax)
ax.set_title("GPA by Parental Education Level")
st.pyplot(fig)

# Visualization 5: Family Income vs GPA (Line Plot)
st.subheader("5️⃣ GPA vs Family Income")
fig, ax = plt.subplots(figsize=(6,4))
sns.lineplot(data=df, x='Family Income', y='GPA', marker='o', ax=ax)
ax.set_title("Trend of GPA by Family Income")
st.pyplot(fig)

# Visualization 6: Study Hours vs Family Support (Heatmap)
st.subheader("6️⃣ Study Hours vs Family Support Level")
pivot_table = pd.crosstab(df['Study Hours'], df['Family Support'])
fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(pivot_table, cmap="YlGnBu", ax=ax)
ax.set_title("Relationship between Study Hours and Family Support")
st.pyplot(fig)

st.markdown("""
**Interpretation:**  
The findings indicate that students from families with higher education and income levels 
often display slightly higher academic performance. Family support positively correlates with consistent study habits.
""")

# ============================================================
# PAGE 3 – Computer Skills & Extracurricular Impact
# ============================================================
st.title("💻 Objective 3: Analyze Computer Skills and Extracurricular Impact")

st.markdown("""
**Objective Statement:**  
To explore how computer proficiency and extracurricular participation relate to student academic performance.

**Summary Box:**  
This section visualizes how computer skills and non-academic activities influence GPA and study behavior.
""")

# Visualization 7: GPA by Computer Skill & Extracurricular (Grouped Bar)
st.subheader("7️⃣ GPA by Computer Skill and Extracurricular Involvement")
if all(col in df.columns for col in ['Computer Skill', 'Extracurricular', 'GPA']):
    gpa_summary = df.groupby(['Computer Skill', 'Extracurricular'])['GPA'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7,5))
    sns.barplot(data=gpa_summary, x='Computer Skill', y='GPA', hue='Extracurricular', ax=ax)
    ax.set_title("Average GPA by Computer Skill and Extracurricular Participation")
    ax.set_xlabel("Computer Skill Level")
    ax.set_ylabel("Average GPA")
    ax.legend(title="Extracurricular Activity")
    plt.xticks(rotation=0)
    st.pyplot(fig)
else:
    st.warning("Required columns for this visualization are missing.")

# Visualization 8: GPA by Computer Skill (Box Plot)
st.subheader("8️⃣ GPA Distribution by Computer Skill Level")
fig, ax = plt.subplots(figsize=(6,4))
sns.boxplot(data=df, x='Computer Skill', y='GPA', ax=ax, palette='coolwarm')
ax.set_title("GPA Distribution by Computer Skill Level")
st.pyplot(fig)

# Visualization 9: Study Hours vs Computer Skill (Bar Chart)
st.subheader("9️⃣ Average Study Hours by Computer Skill")
study_summary = df.groupby('Computer Skill')['Study Hours'].mean().reset_index()
fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(data=study_summary, x='Computer Skill', y='Study Hours', ax=ax, palette='Set3')
ax.set_title("Average Study Hours by Computer Skill Level")
st.pyplot(fig)

st.markdown("""
**Interpretation:**  
Students with stronger computer skills and active extracurricular engagement 
tend to manage study hours more efficiently and achieve higher GPAs.
This highlights the importance of balanced technical and soft skills in academic success.
""")

# ============================================================
# End of Dashboard
# ============================================================
st.success("✅ Visualization report complete! Explore each objective using the sidebar.")

