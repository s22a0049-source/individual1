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

# ======================================

