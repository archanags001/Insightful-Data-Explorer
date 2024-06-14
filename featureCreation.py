import streamlit as st
import pandas as pd
import numpy as np


def createFeature():
    st.write("#### Custom Feature Creation")

    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state:
        st.session_state.df = None

    data = st.session_state.df

    st.subheader("Data Preview")
    st.write(data)

    # Feature Engineering Options
    st.header("Create Custom Features")
    st.write("Select the features and operations to create custom features")

    new_features = []
    # Mathematical Operations between columns
    if st.checkbox("Add new feature by mathematical operations between columns"):
        st.subheader("Mathematical Operations")
        feature1 = st.selectbox("Select first feature", data.select_dtypes(include=[np.number]).columns)
        operation = st.selectbox("Select operation", ['+', '-', '*', '/'])
        feature2 = st.selectbox("Select second feature", data.select_dtypes(include=[np.number]).columns)
        new_feature_name = st.text_input("New feature name")
        
        if st.button("Create Feature"):
            try:
                if operation == '+':
                    data[new_feature_name] = data[feature1] + data[feature2]
                elif operation == '-':
                    data[new_feature_name] = data[feature1] - data[feature2]
                elif operation == '*':
                    data[new_feature_name] = data[feature1] * data[feature2]
                elif operation == '/':
                    data[new_feature_name] = data[feature1] / data[feature2]
                
                st.write(f"Created feature '{new_feature_name}'")
                st.session_state.df  = data
                st.dataframe(st.session_state.df )
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error creating feature: {e}")

    # Mathematical Operations with constants
    if st.checkbox("Add new feature by mathematical operations with constants"):
        st.subheader("Mathematical Operations with Constants")
        feature = st.selectbox("Select feature", data.select_dtypes(include=[np.number]).columns, key="math_ops_feature")
        operation = st.selectbox("Select operation", ['+', '-', '*', '/'],key="math_ops_operation")
        constant = st.number_input("Enter constant value", value=1.0,key="math_ops_constant")
        new_feature_name = st.text_input("New feature name for constant operation",key="math_ops_new_feature_name")
        
        if st.button("Create Feature with Constant"):
            try:
                if operation == '+':
                    data[new_feature_name] = data[feature] + constant
                elif operation == '-':
                    data[new_feature_name] = data[feature] - constant
                elif operation == '*':
                    data[new_feature_name] = data[feature] * constant
                elif operation == '/':
                    data[new_feature_name] = data[feature] / constant
                
                st.write(f"Created feature '{new_feature_name}' with constant operation")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error creating feature with constant: {e}")

    # Log, sqrt, exp transformations
    if st.checkbox("Add new feature by transformations"):
        st.subheader("Transformations")
        feature = st.selectbox("Select feature for transformation", data.select_dtypes(include=[np.number]).columns)
        transformation = st.selectbox("Select transformation", ['log', 'sqrt', 'exp'])
        new_feature_name = st.text_input("New feature name for transformation")
        
        if st.button("Create Transformed Feature"):
            try:
                if transformation == 'log':
                    data[new_feature_name] = np.log(data[feature])
                elif transformation == 'sqrt':
                    data[new_feature_name] = np.sqrt(data[feature])
                elif transformation == 'exp':
                    data[new_feature_name] = np.exp(data[feature])
                
                st.write(f"Created feature '{new_feature_name}' with transformation")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error creating transformed feature: {e}")
    
    # Binning
    if st.checkbox("Add new feature by binning"):
        st.subheader("Binning")
        feature = st.selectbox("Select feature to bin", data.select_dtypes(include=[np.number]).columns)
        bins = st.slider("Number of bins", min_value=2, max_value=10, value=5)
        new_feature_name = st.text_input("New binned feature name")
        
        if st.button("Create Binned Feature"):
            try:
                data[new_feature_name] = pd.cut(data[feature], bins)
                st.write(f"Created binned feature '{new_feature_name}'")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error creating binned feature: {e}")

    # Polynomial Features
    if st.checkbox("Add polynomial features"):
        st.subheader("Polynomial Features")
        feature = st.selectbox("Select feature for polynomial transformation", data.select_dtypes(include=[np.number]).columns)
        degree = st.slider("Degree of polynomial", min_value=2, max_value=5, value=2)
        new_feature_name = st.text_input("New polynomial feature name")
        
        if st.button("Create Polynomial Feature"):
            try:
                data[new_feature_name] = data[feature] ** degree
                st.write(f"Created polynomial feature '{new_feature_name}' with degree {degree}")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error creating polynomial feature: {e}")
    
    # Contaminate Object Columns
    if st.checkbox("Contaminate object columns"):
        st.subheader("Contaminate Object Columns")
        feature = st.selectbox("Select object column to contaminate", data.select_dtypes(include=['object']).columns)
        contamination = st.text_input("Enter contamination string")
        new_feature_name = st.text_input("New feature name for contaminated column")
        
        if st.button("Contaminate Column"):
            try:
                data[new_feature_name] = data[feature] + contamination
                st.write(f"Contaminated column '{new_feature_name}' with string '{contamination}'")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error contaminating column: {e}")

    # Concatenate Object Columns
    if st.checkbox("Concatenate two object columns"):
        st.subheader("Concatenate Object Columns")
        feature1 = st.selectbox("Select first object column", data.select_dtypes(include=['object']).columns)
        feature2 = st.selectbox("Select second object column", data.select_dtypes(include=['object']).columns)
        separator = st.text_input("Separator", value="")
        new_feature_name = st.text_input("New concatenated feature name")
        if st.button("Concatenate Columns"):
            try:
                data[new_feature_name] = data[feature1].astype(str) + separator + data[feature2].astype(str)
                st.write(f"Concatenated columns '{feature1}' and '{feature2}' into '{new_feature_name}' with separator '{separator}'")
                st.session_state.df = data
                st.dataframe(st.session_state.df)
                new_features.append(new_feature_name)
            except Exception as e:
                st.error(f"Error concatenating columns: {e}")

    st.write(new_features)