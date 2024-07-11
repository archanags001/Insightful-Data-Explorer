import streamlit as st
from streamlit_option_menu import option_menu
from home import home_page
from chat_with_data_llm import chatData
from edit_data import edit_dataframe
from data_profiling import stProfile
from visualization import visualizatn
from featureEngineering import feature_engineering
from models_automl import ml_models
from about import about_info
from contact_form import contact

 # Page setup
st.set_page_config(
    page_title="Insightful Data Explorer",
    page_icon="📊",
    layout="wide",
)
# initial_sidebar_state="expanded"
# Header
side_bg_color = "#C0C0C0"
side_text = "#333333"
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)
st.markdown("""
<style>
.navbar {
    display: flex;
    align-items: center;
    justify-content: center;
    # height: 80px; /* Adjust the height as needed */
}
.navbar-brand {
    font-size: 74px;
    # position: absolute;
    # left: 90%;
    # transform: translateX(-0%);

}

</style>
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #C0C0C0;">
    <div class="navbar-brand" target="_blank">
        <span style="color: #333333; font-size: 44px;">   Insightful Data Explorer </span>
    </div>

</nav>
""", unsafe_allow_html=True)
# Function to generate CSS with user-selected colors
def generate_custom_css(side_bg_color, side_text):
    return f"""
    <style>

    /* Sidebar background */
    [data-testid="stSidebar"] > div:first-child {{
    background-color: {side_bg_color};
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: {side_text}; /* Sidebar text color */
    }}

    /* Sidebar additional styles */
    [data-testid="stSidebar"] {{
        background-color: {side_bg_color};
    }}
    .sidebar-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: {side_text};
    }}
    .sidebar-logo {{
        max-width: 150px;
        margin-bottom: 10px;
    }}
    .sidebar-title {{
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: {side_text};
    }}
    .sidebar-menu-item {{
        color: {side_text};
    }}

    /* Header */
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    color: {side_text}; /* Header text color */
    }}
    </style>

    """

m = st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: #1E9E35;
            }
            </style>""", unsafe_allow_html=True)
don_bt = st.markdown("""
    <style>
    .stDownloadButton>button {
        background-color: #1E9E35 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom HTML to increase font size
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    # Initialize session state variables if they don't exist
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state:
        st.session_state.df = None

    # Sidebar content
    with st.sidebar:
        # Other sidebar elements
        st.sidebar.image("logo_image.png", width=300,use_column_width=True)
        # Option menu in sidebar
        pages = ["Home", "Chat with data", "Data Editor", "Profiling", "Visualization", "Feature Engineering", "Auto ML", "About", "Contact"]
        nav_tab_op = option_menu(
            menu_title="Menu",
            options=pages,
            icons=['house', 'chat', 'pencil-square' ,'file-earmark-bar-graph', 'bar-chart-line', 'tools', 'robot', 'info-circle', 'envelope'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important","background-color":"#C0C0C0"},
                "icon": {"color": "#333333", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "color":"#333333","--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

        # User options for selecting background and text color
        st.sidebar.title("Customize Sidebar Appearance")
        side_bg_color = st.sidebar.color_picker("Pick a sidebar background color", "#C0C0C0")
        side_text = st.sidebar.color_picker("Pick a sidebar text color", "#333333")
        # Apply the custom CSS
        custom_css = generate_custom_css(side_bg_color, side_text)
        st.markdown(custom_css, unsafe_allow_html=True)
    # Main content of the app
    if nav_tab_op == "Home":
        home_page()
    elif nav_tab_op == "Chat with data":
        chatData()
    elif nav_tab_op == "Data Editor":
        edit_dataframe()
    elif nav_tab_op == "Profiling":
        stProfile()
    elif nav_tab_op == "Visualization":
        visualizatn()
    elif nav_tab_op == "Feature Engineering":
        feature_engineering()
    elif nav_tab_op == "Auto ML":
        ml_models()
    elif nav_tab_op == "About":
        about_info()
    elif nav_tab_op == "Contact":
        contact()

if __name__ == "__main__":
    main()

