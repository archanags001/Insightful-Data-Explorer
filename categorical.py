import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import category_encoders as ce
from category_encoders import TargetEncoder

def one_hot_encoding(data):
    one_hot_encoder = OneHotEncoder(drop='first',sparse_output=False)
    encoded_data = one_hot_encoder.fit_transform(data)
    feature_names = one_hot_encoder.get_feature_names_out(data.columns)
    encoded_df = pd.DataFrame(encoded_data, columns=feature_names)
    return encoded_df

def label_encoding(data):
    label_encoder = LabelEncoder()
    encoded_data = data.copy()
    for col in data.columns:
        encoded_data[col] = label_encoder.fit_transform(data[col])
    return encoded_data

def ordinal_encoding(data, ordering):
    encoder = OrdinalEncoder(categories=ordering)
    encoded_data = encoder.fit_transform(data)
    encoded_data = pd.DataFrame(encoded_data, columns=data.columns)
    return encoded_data


def target_encoding(data, target):
    target_encoder = TargetEncoder()
    encoded_data = data.copy()
    encoded_data = target_encoder.fit_transform(data, target)
    return encoded_data

def frequency_encoding(data):
    encoded_data = data.copy()
    for col in data.columns:
        freq = data[col].value_counts(normalize=True)
        encoded_data[col] = data[col].map(freq)
    return encoded_data
#


# def ordinal_order(unique_val,start_index ):
#     # Initialize dictionary to store selectboxes
#     selectboxes = {}
#     name_list = sorted(unique_val[start_index])
#     # st.write(name_list.tolist())
#     # # Create selectboxes
#     for i in range(len(unique_val[start_index])):
#         key = f'Select_{i + 1}'
#         if key not in selectboxes:
#             selectboxes[key] = st.selectbox(f'Select order {i + 1}:', name_list)
#             # st.write(selectboxes[key])
#
#         # Update name list based on selected option
#         name_list = [name for name in name_list if name != selectboxes[key]]
#     ordered_val = list(selectboxes.values())
#     return ordered_val


# Function to encode categorical data based on selected technique
def encode_data(data, column, technique, n_features,target,orderd_list):
    encoded_data = data.copy()
    if technique == "Label Encoding":
        encoded_data = label_encoding(data[column])
    elif technique == "One-Hot Encoding":
        encoded_data  = one_hot_encoding(data[column])
    elif technique == "Ordinal Encoding":
        encoded_data = ordinal_encoding(data[column], orderd_list)

    elif technique == "Binary Encoding":
        encoder = ce.BinaryEncoder()
        encoded_data = encoder.fit_transform(data[column])

    elif technique == "Target Encoding":
        encoded_data = target_encoding(data[column],data[target])

    elif technique == "Frequency Encoding":
        encoded_data = frequency_encoding(data[column])

    return encoded_data


def categorical_encoding():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state:
        st.session_state.df = None

    data = st.session_state.df
    orderd_list = []

    # if uploaded_file is not None:
#     data = pd.read_csv(uploaded_file)

    # Display the loaded data
    st.write("Original Data:")
    st.write(data)

    # Select encoding technique
    encoding_technique = st.selectbox('Select the encoding technique:',
                                      ["One-Hot Encoding", "Label Encoding", "Ordinal Encoding", "Binary Encoding",
                                       "Target Encoding", "Frequency Encoding"]
                                      )
    n_features = 1
    target = 0
    if encoding_technique == "Target Encoding":
        target = st.selectbox('Select the target column:', data.select_dtypes(include='number').columns)


    # Select column
    selected_column = st.multiselect('Select the categorical column:', data.select_dtypes(include='object').columns)

    if encoding_technique == "Ordinal Encoding":
        unique_val = []
        orderd_list = []
        st.write("Select the order of columns")
        for col in selected_column:
            unique_val.append(data[col].unique())
        # Calculate the number of rows needed based on the length of unique_val and the desired number of columns
        num_rows = -(-len(unique_val) // 3)  # Ceiling division to ensure all elements are covered

        # Iterate over each row
        # for row in range(num_rows):
        #     col1, col2, col3 = st.columns(3)
        #
        #     # Calculate the index range for the current row
        #     start_index = row * 3
        #     end_index = min((row + 1) * 3, len(unique_val))  # Ensure not to exceed the length of unique_val
        # Iterate over each row
        for row in range(num_rows):
            cols = st.columns(3)

            # Calculate the index range for the current row
            start_index = row * 3

            # Fill in select boxes for each column in the current row
            for i in range(3):
                col_index = start_index + i
                if col_index < len(unique_val):
                    with cols[i]:
                        st.write("Column: ", selected_column[col_index])
                        try:
                            name_list = sorted(unique_val[col_index])
                        except Exception as e:
                            st.error(str(e))
                            st.info("Ensure that your data is free from null values.")

                        selectboxes = {}
                        for j in range(len(name_list)):
                            key = f'Select_{col_index}_{j + 1}_{row}'
                            if key not in selectboxes:
                                selectboxes[key] = st.selectbox(f'Select order {j + 1}:', name_list, key=key)
                            # Update name list based on selected option
                            name_list = [name for name in name_list if name != selectboxes[key]]
                        ordered_val = list(selectboxes.values())
                        orderd_list.append(ordered_val)

            st.write(orderd_list)

    if st.button("Encode"):
        try:
            # Encode data based on selected options
            encoded_data = encode_data(data, selected_column, encoding_technique, n_features,target,orderd_list)
        except Exception as e:
            st.error(str(e))
            st.info("Ensure that your data is free from null values.")

        # Display encoded data
        st.write('Encoded Data:')
        st.write(encoded_data)
        if encoding_technique in ["One-Hot Encoding","Binary Encoding","Hashing Encoder"]:
            encoded_data_final = pd.concat([data, encoded_data], axis=1)
            encoded_data_final.drop(columns=selected_column, inplace=True, axis=1)
        else:
            data.drop(columns=selected_column, inplace=True, axis=1)
            encoded_data_final = pd.concat([data, encoded_data], axis=1)
        st.dataframe(encoded_data_final)
        st.session_state.df = encoded_data_final


