import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Multi-page Data App", layout="centered")

PAGES = {
    "Home": "home",
    "Upload & Preview": "upload",
    "Charts": "charts",
    "About": "about",
}

page = st.sidebar.radio("Navigation", list(PAGES.keys()))

def render_home():
    st.title("Multi-page Streamlit App")
    st.markdown(
        """
        This demo app shows:
        - a file upload & preview page (CSV)
        - simple interactive charts using Altair
        - a small about page

        Use the sidebar to navigate.
        """
    )

def render_upload():
    st.title("Upload & Preview")
    st.write("Upload a CSV file to preview the data and set chart options on the Charts page.")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is None:
        st.info("No file uploaded. You can use the sample dataset button below to load a demo.")
        if st.button("Load sample dataset (iris)"):
            df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
            st.session_state["uploaded_df"] = df
            st.success("Sample dataset loaded into session.")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["uploaded_df"] = df
            st.success(f"Loaded {len(df):,} rows and {len(df.columns):,} columns.")
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")

    if "uploaded_df" in st.session_state:
        df = st.session_state["uploaded_df"]
        st.subheader("Preview")
        st.dataframe(df.head(50))
        with st.expander("Data types and summary (first rows)"):
            st.write(df.dtypes)
            st.write(df.describe(include="all"))

def render_charts():
    st.title("Charts")
    if "uploaded_df" not in st.session_state:
        st.warning("No dataset available. Go to Upload & Preview and upload a CSV or load the sample dataset.")
        return

    df = st.session_state["uploaded_df"]
    st.subheader("Select columns for charting")
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not numeric_columns:
        st.error("No numeric columns found in the dataset for charting.")
        st.dataframe(df.head())
        return

    x_col = st.selectbox("X axis (numeric)", numeric_columns, index=0)
    y_col = st.selectbox("Y axis (numeric)", numeric_columns, index=min(1, len(numeric_columns)-1))
    color_col = st.selectbox("Color (optional)", [None] + categorical_columns)

    st.markdown("### Scatter plot (Altair)")
    base = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X(x_col, type="quantitative"),
        y=alt.Y(y_col, type="quantitative"),
        tooltip=list(df.columns[:6])  # show first few cols in tooltip
    )
    if color_col:
        base = base.encode(color=alt.Color(color_col, legend=alt.Legend(title=color_col)))
    chart = base.interactive()
    st.altair_chart(chart, use_container_width=True)

    st.markdown("### Histogram of X")
    hist = alt.Chart(df).mark_bar().encode(
        alt.X(x_col, bin=alt.Bin(maxbins=40)),
        y='count()'
    ).interactive()
    st.altair_chart(hist, use_container_width=True)

    st.markdown("### Quick stats")
    st.write(df[[x_col, y_col]].describe())

def render_about():
    st.title("About")
    st.markdown(
        """
        - App: Multi-page demo with file upload and Altair charts
        - How it works: Uploaded CSV is stored in session_state under `uploaded_df`.
        - To extend: add more pages, caching, model inference, or downloadable results.
        """
    )

if PAGES[page] == "home":
    render_home()
elif PAGES[page] == "upload":
    render_upload()
elif PAGES[page] == "charts":
    render_charts()
elif PAGES[page] == "about":
    render_about()
else:
    st.error("Page not found.")
