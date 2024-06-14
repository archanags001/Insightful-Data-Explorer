import streamlit as st
from streamlit_option_menu import option_menu



def drop_columns(dataframe, columns_to_drop):
    return dataframe.drop(columns=columns_to_drop, axis=1)
def update(edf):
    edf.to_csv('updated_data.csv', index=False)
    # load_df.clear()


def edit_table(df):
    try:
        edf = st.data_editor(df,num_rows="dynamic",hide_index=False)
    except Exception as e:
        st.error(str(e))
    save_button = st.button('Save')
    if save_button:
        st.session_state.df = edf

def edit_dataframe():
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Please provide the data to proceed.")
        return
    df = st.session_state.df
    st.title("Edit Data")
    st.write("The Data Editor page provides two main functionalities to help you manage and refine your dataset:")
    st.markdown("""
    1. **Edit Table**: In this tab, you can directly interact with your dataset using 
    [Streamlit's Data Editor](https://data-editor.streamlit.app). This allows you to:
        - View your dataset in a tabular format.
        - Make changes directly to individual cells.
        - Add or delete rows as needed.
          - **Add new row**: Go to the lower end of the table and click the "+" symbol.
          - **Delete row**: Select the rows from the left end (the first column) and then click on the trash symbol above 
          the table.
        - Save your changes for further analysis.
    2. **Drop Columns**: In this tab, you have the ability to remove unwanted columns from your dataset.
    (If you need to add new columns, go to the Feature Engineering tab and then to the Feature Creation tab).
    """)
    st.write(" ")
    pages = ["Edit Table","Drop column"]
    edit_tab_op = option_menu(
        menu_title="Edit",
        options=pages,
        icons=['pencil-square', 'trash'],
        menu_icon="list",
        default_index=0,
        orientation='horizontal',
    )
    if edit_tab_op == "Edit Table":
        edit_table(df)
    elif edit_tab_op == "Drop column":
        # Multiselect to choose columns to drop
        columns_to_drop = st.multiselect("Select columns to drop", df.columns)

        # Drop button
        if st.button("Drop Columns"):
            if columns_to_drop:
                try:
                    # Drop the selected columns
                    df = drop_columns(df, columns_to_drop)
                    st.success(f"Columns {columns_to_drop} dropped successfully!")
                    # Display the updated dataframe
                    st.session_state.df = df
                    st.write("Updated Dataframe:")
                    st.dataframe(df)
                except Exception as e:
                    st.error(str(e))

            else:
                st.warning("No columns selected to drop")