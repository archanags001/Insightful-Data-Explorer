import streamlit as st
from streamlit_option_menu import option_menu
from pygwalker.api.streamlit import StreamlitRenderer
from auto_viz import autoVizs

def pywalkr(dataset):
    try:
        pyg_app = StreamlitRenderer(dataset)
        pyg_app.explorer()
    except Exception as e:
        st.error(str(e))
def visualizatn():

    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Please provide the data to proceed.")
        return
    st.title("Visualization")
    st.markdown("""
    Explore your data visually with two powerful tools:

    **Custom Visualization** : Create personalized charts and graphs using [pygwalker](https://kanaries.net/pygwalker)

   **Auto Visualization** : Automatically generate a variety of insightful visualizations with 
    [AutoViz](https://pypi.org/project/autoviz/0.0.6/)
    """)

    dataset = st.session_state.df
    viz_tab_op = option_menu(
        menu_title="Visualization",
        options=["Custom Visualization", "Auto Visualization"],
        orientation='horizontal',
    )
    if viz_tab_op == "Auto Visualization":
        autoVizs()
    elif viz_tab_op == "Custom Visualization":
        pywalkr(dataset)

