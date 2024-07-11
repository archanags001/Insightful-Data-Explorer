import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
def stProfile():

    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Please provide the data to proceed.")
        return
    st.title("Pandas Profiling")
    st.markdown("""

        This page provides an in-depth analysis of your dataset using 
        [YData Profiling](https://docs.profiling.ydata.ai/latest/).  Gain insights into data 
        distributions, correlations, missing values, and more with just a few clicks.
        """)
    st.info("Please note that there may be a processing delay during data profiling.")

    dataset = st.session_state.df
    if len(dataset) > 0:
        profile_report = ProfileReport(dataset)
        export = profile_report.to_html()
        st.download_button(label="Download Full Report", data=export, file_name='report.html')
        st_profile_report(profile_report)

