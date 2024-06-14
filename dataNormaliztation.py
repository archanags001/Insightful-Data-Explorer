import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer


# Function to perform data normalization based on selected technique
def normalize_data(data, columns_to_normalize, technique):
    numeric_columns = data.select_dtypes(include=['number']).columns
    columns_to_normalize = [col for col in columns_to_normalize if col in numeric_columns]

    if technique == 'Min-Max Scaling':
        scaler = MinMaxScaler()
    elif technique == 'Standardization':
        scaler = StandardScaler()
    elif technique == 'Robust Scaling':
        scaler = RobustScaler()
    elif technique == 'Normalization':
        scaler = Normalizer()
    elif technique == 'Log Transformation':
        data[columns_to_normalize] = data[columns_to_normalize].apply(lambda x: np.log1p(x))
        return data
    else:
        return data

    data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])
    return data


def data_normalization():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state:
        st.session_state.df = None

    data = st.session_state.df

    st.write("Data:")
    st.dataframe(data)

    # Column selection for normalization
    numeric_columns = data.select_dtypes(include=['number']).columns
    columns_to_normalize = st.multiselect("Select columns to normalize:", numeric_columns)

    # Data normalization technique selection
    techniques = ['Min-Max Scaling', 'Standardization', 'Robust Scaling', 'Normalization', 'Log Transformation']
    technique = st.selectbox("Select normalization technique:", techniques)

    # Perform normalization and display results
    if st.button("Normalize Data"):
        try:
            normalized_data = normalize_data(data.copy(), columns_to_normalize, technique)
            st.session_state.df = normalized_data
            st.write("Normalized Data:")
            st.dataframe(st.session_state.df)
        except ValueError as e:
            st.error(str(e))


