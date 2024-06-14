import streamlit as st
import numpy as np
from scipy.stats import zscore, iqr,boxcox
from sklearn.covariance import EllipticEnvelope
from statsmodels.robust import mad
from sklearn.cluster import DBSCAN
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from streamlit_option_menu import option_menu
from scipy.stats.mstats import winsorize



def zscore_outliers(data):
    try:
        z_scores = np.abs(zscore(data))
        return np.where(z_scores > 3)[0]
    except ValueError as e:
        msg = "An error occurred while applying zscore method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")


def iqr_outliers(data):
    try:
        q1, q3 = np.percentile(data, [25, 75])
        iqr_val = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr_val, q3 + 1.5 * iqr_val
        return np.where((data < lower_bound) | (data > upper_bound))[0]
    except ValueError as e:
        msg = "An error occurred while applying IQR method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")



def mahalanobis_outliers(data):
    try:
        clf = EllipticEnvelope(contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]
    except ValueError as e:
        msg = "An error occurred while applying Mahalanobis method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")


def mad_outliers(data):
    try:
        median = np.median(data)
        mad_value = mad(data)
        threshold = 3 * mad_value
        return np.where(np.abs(data - median) > threshold)[0]

    except ValueError as e:
        msg = "An error occurred while applying MAD method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")


def knn_outliers(data):
    try :
        clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]

    except ValueError as e:
        msg = "An error occurred while applying KNN method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")


def isolation_forest_outliers(data):
    try:
        clf = IsolationForest(contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]
    except ValueError as e:
        msg = "An error occurred while applying Isolation_forest method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")


def dbscan_outliers(data):
    try:
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        data['cluster'] = dbscan.fit_predict(data.values)
        return np.where(data['cluster'] == -1)[0]
    except ValueError as e:
        msg = "An error occurred while applying DBSCAN method,\n ERROR:  "+str(e)
        st.error(msg)
        st.info("Please check your data or try a different outlier detection method.")





def outlier_detection():

    st.title("Outlier Detection")

    if st.session_state.df is not None:
        cols = st.columns(2)
        outlier_method = cols[1].selectbox(
            "Select Outlier Detection Method",
            ["Z-Score", "IQR", "Mahalanobis", "MAD", "DBSCAN", "KNN", "Isolation Forest"]
        )

        column_selector = cols[0].multiselect(
            "Select Column for Outlier Detection",
            st.session_state.df.select_dtypes(include=np.number).columns
        )
        st.session_state.column_selector = column_selector

        # Check if at least one column is selected
        if not column_selector:
            st.info("Please ensure that at least one column is selected")
            return
        outliers = None
        error_msg = None


        if outlier_method == "Z-Score":
            outliers = zscore_outliers(st.session_state.df[column_selector])
        elif outlier_method == "IQR":
            outliers = iqr_outliers(st.session_state.df[column_selector])
        elif outlier_method == "Mahalanobis":
            outliers = mahalanobis_outliers(st.session_state.df[column_selector])
        elif outlier_method == "MAD":
            outliers = mad_outliers(st.session_state.df[column_selector])
        elif outlier_method == "DBSCAN":
            outliers = dbscan_outliers(st.session_state.df[column_selector])
        elif outlier_method == "KNN":
            outliers = knn_outliers(st.session_state.df[column_selector])
        elif outlier_method == "Isolation Forest":
            outliers = isolation_forest_outliers(st.session_state.df[column_selector])

        st.session_state.outliers =outliers




        # Display outliers with highlighted columns
        st.subheader(f"Outliers using {outlier_method} for {column_selector}:")
        try:
            st.write("Number of outliers: ", len(st.session_state.outliers))

            st.dataframe(st.session_state.df.loc[outliers].style.set_properties(**{'background-color': '#F4CABC'},
                                                                            subset=column_selector))
            st.subheader("Lightcoral color highlights data points with outliers.")
            st.dataframe(
                st.session_state.df.style.applymap(
                    lambda _: "background-color: lightcoral;", subset=(outliers, slice(None))
                )
            )
        except Exception as e:
            msg = "An error occurred while applying "+ outlier_method + " method,\n ERROR:  "+str(e)
            st.error(msg)
            st.info("Please check your data or try a different outlier detection method.")
        except ValueError :
            msg = "An error occurred while applying "+ outlier_method + " method,\n ERROR:  "
            st.error(msg)
            st.info("Please check your data or try a different outlier detection method.")
        except TypeError :
            msg = "An error occurred while applying "+ outlier_method + " method,\n ERROR:  "
            st.error(msg)
            st.info("Please check your data or try a different outlier detection method.")
        except:
            st.error("Unexpected error:")



def handle_outliers_tech(data, method, column_selector, outliers,min_max_list,bounds,imputation_value):
    if method == "Log Transformation":
        for column in column_selector:
            data[column], _ = boxcox(data[column])
    elif method == "Box-Cox Transformation":
        for column in column_selector:
            data[column], fitted_lambda = boxcox(data[column])
            st.write(f"Lambda value used for {column} Transformation: ", fitted_lambda)
    elif method == "Truncation or Capping":
        i = 0
        for column in column_selector:
            data[column] = np.clip(data[column], a_min=min_max_list[i][0], a_max=min_max_list[i][1])
            i+=1
    elif method == "Winsorizing":
        i = 0
        for column in column_selector:
            data[column] = winsorize(data[column], limits=(bounds[i][0], bounds[i][1]))
            i+=1
    elif method == "Imputation":
        i =0
        for col in column_selector:
            data.loc[outliers, col] = np.nan
            data[col] = data[col].fillna(imputation_value[i])
            i+=1
    elif method == "Remove Outliers":
        data = data.drop(outliers, axis=0).reset_index(drop=True)
    return data

def outlier_handling():
    st.title("Outlier Handling")

    if st.session_state.df is not None:
        cols = st.columns(2)
        handle_option = cols[0].selectbox("Select Outlier Handling Technique",
                                           ["None", "Log Transformation", "Box-Cox Transformation",
                                            "Truncation or Capping", "Winsorizing", "Imputation", "Remove Outliers"])
        if handle_option is None:
            st.warning("Please ensure that at least one technique is selected")


        if handle_option != "Remove Outliers":
            column_selector_handle = cols[1].multiselect("Select Column to handle Outlier", st.session_state.column_selector)
        else:
            column_selector_handle = st.session_state.column_selector
        imputation_value =[]
        bounds = []
        min_max_list = []
        if handle_option =="Imputation":
            for col in column_selector_handle:
                msg = col+": Enter imputation value:"
                imputation_value.append(st.number_input(msg, min_value=-1.7976931348623157e+308,
                                               max_value=1.7976931348623157e+308))
        elif handle_option== "Truncation or Capping":
            for column in column_selector_handle:
                min_max = []
                min_max.append(st.number_input(f"Enter min value for {column}:", min_value=0.0))
                min_max.append(st.number_input(f"Enter max valuefor {column}:", min_value=0.0))
                min_max_list.append(min_max)

        elif handle_option == "Winsorizing":
            for column in column_selector_handle:
                lower_upper = []
                lower_upper.append(st.number_input(f"Enter lower bound value for {column}:", min_value=0.0, max_value=1.0,
                                              key=f"Winsorizing_lower_{column}"))
                lower_upper.append(st.number_input(f"Enter upper bound value for {column}:", min_value=0.0, max_value=1.0,
                                              key=f"Winsorizing_upper_{column}"))
                bounds.append(lower_upper)



        if handle_option != "None":

            if st.button("Handle Outlier"):

                try:

                    st.session_state.df = handle_outliers_tech(st.session_state.df, handle_option,
                                                          column_selector_handle, st.session_state.outliers,
                                                               min_max_list,bounds,imputation_value)
                    outlierfix = list(set(st.session_state.outliers).intersection(st.session_state.df.index))
                    st.dataframe(
                        st.session_state.df.style.applymap(
                            lambda _: "background-color: green;", subset=(outlierfix, slice(None))
                        )
                    )
                except Exception as e:
                    st.error(str(e))


def outlier_detection_handling():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state:
        st.session_state.df = None

        # Define page navigation
    pages = ["Outlier Detection", "Handling Outliers"]
    # st.session_state.page = st.sidebar.radio("Select a page", pages, index=pages.index(st.session_state.page))

    nav_tab_op = option_menu(
        menu_title="",
        options=pages,
        orientation='horizontal',
    )

    if nav_tab_op == "Outlier Detection":
        outlier_detection()
    elif nav_tab_op == "Handling Outliers":
        outlier_handling()











