import streamlit as st

def about_info():
    st.title("About This App")

    st.markdown("""
    **Insightful Data Explorer aims to simplify the data analysis and machine learning process by providing a 
    user-friendly interface with various features**

    ### Key Features:
    - **Data Handling**: Upload CSV or Excel files, edit data, and perform preprocessing tasks such as imputation 
    and outlier handling.
    - **Visualization**: Explore data visually using custom and automated visualization tools.
    - **Feature Engineering**: Transform and create new features to enhance model performance.
    - **AutoML**: Automatically build and compare machine learning models for regression, classification, clustering, 
    anomaly detection, and time series forecasting using PyCaret.

   ### Technologies:
    - **[AutoViz](https://pypi.org/project/autoviz/0.0.6/)**: Provides automated chart selection for quick data 
    exploration.
    - **[PyCaret](https://pycaret.org)**: Powers the AutoML capabilities for model building and optimization.
    - **[pygwalker](https://kanaries.net/pygwalker)**: Enables customizable data visualizations to gain deeper insights
    - **[Streamlit](https://streamlit.io)**: Used for creating interactive and responsive user interfaces.
    
    
    ### Created By:
    ##### **Archana**: [LinkedIn Profile](https://www.linkedin.com/in/archanags001)
    
    
    ### Contact Us:
    For inquiries or feedback, please contact **archanags203@gmail.com**
    

    ### Disclaimer:
    This app is for demonstration and educational purposes only. Use the results and insights responsibly.
    """)


