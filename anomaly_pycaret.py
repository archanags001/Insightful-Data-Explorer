import streamlit as st
import pandas as pd
from pycaret.anomaly import setup, predict_model, pull, plot_model, create_model, models, assign_model, save_model

def anomalyPycaret():
    # st.title("AutoML Using Pycaret")
    st.subheader("AutoML - Anomaly detection")
    if 'begin_ad' not in st.session_state:
        st.session_state.begin_ad = False

    if not st.session_state.begin_ad:
        st.info("To get started, double-click on the Begin button.")
        if st.button(" Begin "):
            st.session_state.begin_ad = True
            st.session_state.button_clicked_ad = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("To restart AutoML, click on the 'Reset' button.")
        if st.button("Reset"):
            st.session_state.begin_ad = True
            st.session_state.button_clicked_ad = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()

        dataset = st.session_state.df
        anomaly_model =''
        # from pycaret.datasets import get_data
        # dataset = get_data('mice')
        if len(dataset) > 0:
            st.write("### Data Preview")
            st.write(dataset)

            # st.header("Dataset Configuration")
            # Initialize session state variables
            if 'form_submitted' not in st.session_state:
                st.session_state.form_submitted = False
            if 'model_saved' not in st.session_state:
                st.session_state.model_saved = False

            st.write("### Model Selection and Configuration")
            with st.form("model_form"):
                features = st.multiselect("Select features to include:", dataset.columns)

                train_size = st.slider("Set the training data size:", 0.1, 0.9, 0.8)
                # validation_size = col2.slider("Set the validation data size:", 0.1, 0.9 - train_size, 0.1)
                st.markdown(
                    '<p style="color:#3355FF">Click the button below to confirm '
                    'your selection before filling out the other fields.</p>', unsafe_allow_html=True)

                change_ad = st.form_submit_button("Click here to confirm your selection")
                if change_ad:
                    st.session_state.form_submitted = False
                if features:
                    # Split data
                    data = dataset[features].sample(frac=train_size, random_state=786).reset_index(drop=True)
                    data_unseen = dataset[features].drop(data.index).reset_index(drop=True)
                    # Setup PyCaret clustering
                    try:
                        s = setup(data, session_id=123)
                    except Exception as e:
                        st.error(str(e))
                    model_df = models()
                    if not model_df.empty:
                        anomaly_model = st.selectbox("Choose the model name", model_df['Name'].tolist())
                        # st.write(" ")
                        # selected_metrics = st.multiselect("Select metrics to evaluate",
                        #                                   options=list(metrics_dict.keys()))
                        st.write(" ")
                        uploaded_file_test = st.file_uploader("If you want to upload a test dataset, upload CSV or Excel test (optional) "
                                                              "file",type=["csv", "xlsx"], key='test')
                        st.write(" ")

                        submit_button = st.form_submit_button("AutoML")

                        if submit_button:
                            st.session_state.form_submitted = True

            # Process form submission and display download button
            if st.session_state.form_submitted and st.session_state.begin_ad:
                st.markdown('<p style="color:#4FFF33">Setup Successfully Completed!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                # st.write("Model created")
                try:
                    model_id = model_df[model_df['Name'] == anomaly_model].index[0]
                    created_model = create_model(model_id)
                    # st.write(pull())
                    st.write("#### Assign")
                    assigned_result = assign_model(created_model)
                    st.dataframe(assigned_result)
                    # save model
                    save_model(created_model, 'anomaly_model')
                    st.write("#### t-SNE (3d) Dimension Plot")
                    with st.spinner("Running......"):
                        try:
                            plot_model(created_model, plot='tsne', display_format='streamlit')
                        except:
                            st.write("The plot is unavailable; please consider using alternative model.")
    
                        try:
                            # Predicts label on the holdout set.
                            pred_holdout = predict_model(created_model, data_unseen)
                            st.write('#### Predictions from holdout set (validation set)')
                            st.dataframe(pred_holdout)
                        except:
                            st.error("Something went wrong, please try other models")
                    # else:
                #     st.warning("Choose the models")

                    if uploaded_file_test:
                        st.write('### Test data')
                        if uploaded_file_test.name.endswith('.csv'):
                            test_dataset = pd.read_csv(uploaded_file_test)
                        elif uploaded_file_test.name.endswith(('.xlsx', '.xls')):
                            test_dataset = pd.read_excel(uploaded_file_test)
                        st.write("Test Data Preview:")
                        # st.write(test_dataset)
                        # test_dataset = pd.read_csv(uploaded_file_test)
                        st.dataframe(test_dataset)
                        test_dataset = test_dataset[features]
                        # test_pred = predict_model(created_model, test_dataset)
                        # st.write("### Prediction")
                        # st.dataframe(test_pred)
                        try:
                            test_pred = predict_model(created_model, test_dataset)
                            st.write("### Prediction")
                            st.dataframe(test_pred)
                        except:
                            st.error("Something went wrong, please try other models")

                    st.session_state.model_saved = True
                except:
                    st.error("Something went wrong, please try other models")

            # Display download button if model is saved
            if st.session_state.model_saved:
                with open('anomaly_model.pkl', 'rb') as f:
                    st.download_button(
                        label="Download Model",
                        data=f,
                        file_name='anomaly_model.pkl',
                        mime='application/octet-stream'
                    )
