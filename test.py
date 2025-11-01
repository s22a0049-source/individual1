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

