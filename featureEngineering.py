import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from sklearn.impute import SimpleImputer, KNNImputer
import numpy as np
from outlierHandling import outlier_detection_handling
from categorical import categorical_encoding
from dataNormaliztation import data_normalization
from featureCreation import createFeature




# Function to perform random imputation for numerical and categorical columns
# def random_impute(data, column_name, dtype):
#     if dtype == 'numerical':
#         data[column_name] = data[column_name].apply(lambda x: np.random.choice(data[column_name].dropna()) if pd.isnull(x) else x)
#     elif dtype == 'categorical':
#         data[column_name] = data[column_name].apply(lambda x: np.random.choice(data[column_name].dropna()) if pd.isnull(x) else x)
#     return data


# Function to perform imputation
def impute_data_2(data, column_name, imputation_method,n_neighbor, cons_var):
    if imputation_method == 'next':
        st.write("Fill values by propagating the last valid observation to next valid.")
        data[column_name] = data[column_name].fillna(method='ffill')
    elif imputation_method == 'previous':
        # Fill values by using the next valid observation to fill the gap.
        data[column_name] = data[column_name].fillna(method='bfill')
    elif imputation_method == 'knn':
        knn_imputer = KNNImputer(n_neighbors=n_neighbor)
        data[column_name] = knn_imputer.fit_transform(data[[column_name]])
    elif imputation_method == 'max':
        data[column_name] = data[column_name].fillna(data[column_name].max())
    elif imputation_method == 'min':
        data[column_name] = data[column_name].fillna(data[column_name].min())
    elif imputation_method == 'most_frequent':
        data[column_name] = data[column_name].fillna(data[column_name].mode().iloc[0])
    elif imputation_method == 'mean':
        data[column_name] = data[column_name].fillna(data[column_name].mean())
    elif imputation_method == 'median':
        data[column_name] = data[column_name].fillna(data[column_name].median())
    elif imputation_method == 'mode':
        data[column_name] = data[column_name].fillna(data[column_name].mode().iloc[0])
    elif imputation_method == 'constant':
        data[column_name] = data[column_name].fillna(cons_var)
    elif imputation_method == 'random':
        data[column_name] = data[column_name].apply(lambda x: np.random.choice(data[column_name].dropna()) if pd.isnull(x) else x)
    elif imputation_method == 'interpolation':
        data[column_name] = data[column_name].interpolate(method='linear', limit_direction='both')
    elif imputation_method == 'extrapolation':
        data[column_name] = data[column_name].interpolate(method='linear', limit_direction='forward')

    elif imputation_method == 'Drop Selected Column':
         data.drop(columns=[column_name],inplace=True)
    elif imputation_method == 'Drop Rows with Null Values':

        data = data.dropna(axis=0,subset=[column_name])
        data = data.reset_index(drop=True)
    else:
        st.warning(f"Unsupported imputation method: {imputation_method}")

    return data



# Streamlit app
def imputation_tab():
    st.title("Imputation App")

    # Upload dataset
    # uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if st.session_state.df is not None:
        # data = pd.read_csv(uploaded_file)

        st.subheader("1. Choose Column:")
        column_name = st.selectbox("Select a column for imputation", st.session_state.df.columns)

        st.subheader(f"2. Number of Missing Values in {column_name}:")
        missing_values_count = st.session_state.df[column_name].isnull().sum()
        st.write(f"There are {missing_values_count} missing values in the selected column.")


        st.subheader("3. Choose Imputation Method:")
        column_dtype = str(st.session_state.df[column_name].dtype)
        imputation_methods = {
            'int64': ['mean', 'median', 'constant', 'most_frequent', 'random','interpolation','extrapolation', 'min',
                      'max' , 'previous','next','knn','Drop Selected Column','Drop Rows with Null Values'],
            'float64': ['mean', 'median', 'constant', 'most_frequent', 'random','interpolation','extrapolation', 'min',
                        'max' , 'previous','next','knn','Drop Selected Column','Drop Rows with Null Values'],
            'object': ['most_frequent', 'constant', 'random','previous','next','Drop Selected Column',
                       'Drop Rows with Null Values' ],
            'datetime64[ns]': ['most_frequent', 'constant', 'random','previous','next','Drop Selected Column',
                               'Drop Rows with Null Values' ]
        }

        if column_dtype in imputation_methods:


            imputation_method = st.selectbox("Select imputation method", imputation_methods[column_dtype])
        else:
            st.warning("No imputation method available for the selected datatype.")
        if imputation_method == 'knn':
            n_neighbor = st.number_input("Select the number of neighbors to be considered for KNN",value=2, step=1)
        else:
            n_neighbor=2
        cons_var = None  # Initialize cons_var with a default value
        if imputation_method == 'constant':

            if st.session_state.df[column_name].dtype == ['float64', 'int64']:
                cons_var = st.number_input("Enter a constant value")
            else:
                cons_var = st.text_input("Enter a constant value")

        st.subheader("4. Impute Data:")
        if st.button("Impute Data"):

            st.session_state.df = impute_data_2(st.session_state.df, column_name, imputation_method,n_neighbor,cons_var)
            st.success("Data imputed successfully!")

        st.subheader("5. Display Data after Imputation:")
        st.dataframe(st.session_state.df)

def change_data_type():
    st.title("Change Data Type")
    df_copy = st.session_state.df.copy()
    dtypes_df = pd.DataFrame(st.session_state.df.dtypes, columns=['Data Type']).reset_index()

    column = st.selectbox("Select column", st.session_state.df.columns, key="column_select")
    new_type = st.selectbox("Select new data type", ["float", "int", "object", "bool", "datetime64[ns]"],
                            key="type_select")

    if st.button('Change Data Type'):
        if new_type == "object":
                # Handle case where user chooses 'object' type
                st.warning("Changing to 'object' type may lead to loss of numerical information.")
                st.session_state.df[column] = st.session_state.df[column].astype(new_type)

        elif new_type == "float" or new_type == "int":
            # Handle conversion for numbers with commas
            try:
                st.session_state.df[column] = st.session_state.df[column].replace(',', '', regex=True).astype(new_type)
                st.success(f"Column {column} converted to {new_type}")
            except Exception as e:
                st.error(f"Error changing data type: {e}")

        elif new_type == "datetime64[ns]":
            # df_copy = st.session_state.df.copy()
            try:
                st.session_state.df[column] = pd.to_datetime(st.session_state.df[column], errors='coerce')
                st.success(f"Column {column} converted to {new_type}")

            except Exception as e:
                st.error(f"Error changing data type: {e}")

    col1,col2 = st.columns(2)
    with col1:
        st.write("Current Data Types:")
        st.write(df_copy.dtypes)
    with col2:

        st.write("Updated Data Types:")
        st.write(st.session_state.df.dtypes)
        # st.write(st.session_state.df)
def remove_duplicates():
    num_duplicates = st.session_state.df.duplicated().sum()
    st.write(f"Total number of duplicate rows in the data: ",num_duplicates)
    if num_duplicates > 0:
        st.write("Would you like to remove these duplicate rows?")
        if st.button("Remove Duplicates"):
            st.session_state.df = st.session_state.df.drop_duplicates()
            st.write("Duplicate rows have been removed. Here's the summary of the cleaned data:")
            st.dataframe(st.session_state.df.describe())
            return st.session_state.df

def feature_engineering():
    # Initialize session state variables if they don't exist
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Please provide the data to proceed.")
        return
    st.title("Feature Engineering")
    st.markdown("""
    Enhance your dataset with various transformations using the following tabs:

    - **Change Data Type**: Modify the data types of columns to suit your analysis needs.
    - **Drop Duplicates**: Remove duplicate rows from your dataset for cleaner data.
    - **Imputation**: Fill in missing values using appropriate strategies.
    - **Handling Outliers**: Address outliers in your data to improve model performance.
    - **Handling Categorical Data**: Encode categorical variables for machine learning algorithms.
    - **Data Normalization**: Scale numerical data to a standard range for better model performance.
    - **Feature Creation**: Generate new features derived from existing ones to capture more information.

    Explore each tab to preprocess your data effectively for analysis and modeling.
    """)
    st.write("")
    # Define page navigation
    pages = ["Change Data Type", "Drop duplicates", "Imputation", "Handling Outliers", "Handling Categorical Data",
             "Data Normalization", "Feature Creation"]
    # st.session_state.page = st.sidebar.radio("Select a page", pages, index=pages.index(st.session_state.page))

    nav_tab_op = option_menu(
        menu_title="",
        options=pages,
        orientation='horizontal',
    )

    if nav_tab_op == "Change Data Type":
        change_data_type()
    elif nav_tab_op == "Drop duplicates":
        remove_duplicates()
    elif nav_tab_op == "Imputation":
        imputation_tab()
    elif nav_tab_op == "Handling Outliers":
        outlier_detection_handling()
    elif nav_tab_op == "Handling Categorical Data":
        categorical_encoding()
    elif nav_tab_op == "Data Normalization":
        data_normalization()
    elif nav_tab_op == "Feature Creation":
        createFeature()


if __name__ == "__main__":
    feature_engineering()




