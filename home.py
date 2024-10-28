import streamlit as st
import pandas as pd
from pycaret.datasets import get_data

def upload_and_preview_data():
    uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", key="file_uploader", type=["csv","xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    st.error(str(e))
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                try:
                    df = pd.read_excel(uploaded_file)
                except Exception as e:
                    st.error(str(e))
            # st.write("Data Preview:")
            # st.write(df)
            return df
        except Exception as e:
            st.error(f"Error reading file: {e}")
    return st.session_state.df


def select_sample_data_page():
    st.subheader("Select a Sample Dataset")
    sample_data_options = ["iris", "wine", "boston", "diabetes", "heart",
                           "titanic", "energy", "airline", "traffic", "concrete", ]
    st.session_state.dataset_name = st.selectbox("Choose a dataset", sample_data_options)

    if st.button("Load Dataset"):
        if st.session_state.dataset_name == "airline":
            data = pd.DataFrame(get_data(st.session_state.dataset_name))
            data = data.reset_index()
        else:
            data = get_data(st.session_state.dataset_name)

        if data is not None:
            return data
        else:
            st.write("Select a Sample Dataset")

def home_page():
    # App title and description
    st.title("Welcome to the Insightful Data Explorer!")

    st.markdown("""
        ### Your One-Stop Solution for Data Handling and Analysis

        **Insightful Data Explorer** simplifies the data analysis and machine learning process through a user-friendly 
        interface. Effortlessly upload, interact with, edit, visualize, and engineer features from your data without coding. Explore 
        the capabilities of automated machine learning (AutoML) to effortlessly build predictive models.

        #### Features:
        - **Upload Data:** Easily upload your data in CSV or Excel format.
        - **Chat with Data:** InsightBot allows you to chat with your data.
        - **Edit Data:** Make changes to your dataset right from the app.
        - **Data Visualization:** Create insightful visualizations to understand your data better.
        - **Feature Engineering:** Perform various feature engineering techniques to prepare your data for modeling.
        - **AutoML:** Use automated machine learning to create predictive models without writing a single line of code.
        """)
    st.info("Disclaimer: The service may be unavailable if too many people use it concurrently. Thank you for your understanding.")
    st.markdown("##### If you're new to this app, this tutorial [video](https://youtu.be/dwlE4p2uF6k) will be very helpful.")
    # Initialize session state
    if 'startbutton' not in st.session_state:
        st.session_state.startbutton = False
    if 'df' not in st.session_state:
        st.session_state.df = None
    start_col1,start_col2 = st.columns(2)
    start_col1.markdown('<p style="color:#4FFF33; font-size: 22px; text-align: right;">To begin, click the button</p>',
                        unsafe_allow_html=True)

    start_button = start_col2.button(" Let's Start ")
    if start_button:
        st.session_state.startbutton = True

    if st.session_state.startbutton:
        file_or_not = st.radio("Do you have your own data?",["Yes","No"])
        if file_or_not == "Yes":
            st.session_state.df = upload_and_preview_data()
        elif file_or_not == "No":
            st.session_state.df = select_sample_data_page()
        if st.session_state.df is not None:
            st.write("Data Preview:")
            st.write(st.session_state.df)

    st.markdown(""" 
        #### How to Use: 
        1. **Upload Your Data:** Click on the 'Start' button to upload your CSV or Excel file.
        2. **Chat with Data:** Type your questions regarding the loaded data. InsightBot will provide answers to your queries. If you're not satisfied with the response, please ask again.
        3. **Edit Your Data:** Navigate to the 'Data Edit' tab to make modifications to your dataset.
        4. **Visualize Your Data:** Use the 'Visualization' tab to generate different types of charts and graphs.
        5. **Feature Engineering:** Go to the 'Feature Engineering' tab to create and modify features.
        6. **AutoML:** Visit the 'AutoML' tab to automatically train and evaluate machine learning models.

        Get started by selecting an option from the sidebar!

        If you have any questions or need assistance, feel free to reach out to .

        **Happy Data Analyzing!**

        ---
        """)




