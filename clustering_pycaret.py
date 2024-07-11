import streamlit as st
import pandas as pd
from pycaret.clustering import setup, predict_model, pull, plot_model, create_model,models,assign_model,save_model


# Dictionary of metrics
metrics_dict = {
    "Cluster PCA Plot (2d)": 'cluster',
    "Cluster TSnE (3d)": 'tsne',
    "Elbow Plot": 'elbow',
    "Silhouette Plot": 'silhouette',
    "Distance Plot": 'distance',
    "Distribution Plot": 'distribution'
}
fig_kwargs = {
                    "renderer": "png",
                    "width": 1000,
                    "height": 400,
                }

def clusteringPycaret():
    st.subheader("AutoML - Clustering")
    if 'begin_clu' not in st.session_state:
        st.session_state.begin_clu = False

    if not st.session_state.begin_clu:
        st.info("To get started, double-click on the Begin button.")
        if st.button(" Begin "):
            st.session_state.begin_clu = True
            st.session_state.button_clicked = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("To restart AutoML, click on the 'Reset' button.")
        if st.button("Reset"):
            st.session_state.begin_clu = True
            st.session_state.button_clicked = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()
        dataset = st.session_state.df
        if len(dataset) > 0:
            st.write("### Data Preview")
            st.write(dataset)

            # Initialize session state variables
            if 'form_submitted' not in st.session_state:
                st.session_state.form_submitted = False
            if 'model_saved' not in st.session_state:
                st.session_state.model_saved = False
            # model_df = models()
            st.write("### Model Selection and Configuration")
            with st.form("model_form"):
                features = dataset.columns
                features = st.multiselect("Select features to include:", dataset.columns)
                # col1, col2 = st.columns(2)
                train_size = st.slider("Set the training data size:", 0.1, 0.9, 0.8)
                # validation_size = col2.slider("Set the validation data size:", 0.1, 0.9 - train_size, 0.1)
                st.markdown(
                    '<p style="color:#3355FF">Click the button below to confirm '
                    'your selection before filling out the other fields.</p>', unsafe_allow_html=True)

                change_clu = st.form_submit_button("Click here to confirm your selection")
                if change_clu:
                    st.session_state.form_submitted = False
                if features:
                    # Split data
                    data = dataset[features].sample(frac=train_size, random_state=786).reset_index(drop=True)
                    data_unseen = dataset[features].drop(data.index).reset_index(drop=True)
                    try:
                        s = setup(data, session_id=123)
                    except Exception as e:
                        st.error(str(e))
                    model_df = models()
                    if not model_df.empty:
                        cluster_model = st.selectbox("Choose the model name", model_df['Name'].tolist())
                        num_clusters = st.slider("Set number of clusters (optinal):", 1, 100, 1)
                        st.write(" ")
                        selected_metrics = st.multiselect("Select classification metrics to evaluate",
                                                          options=list(metrics_dict.keys()))
                        st.write(" ")
                        uploaded_file_test = st.file_uploader("If you want to upload a test dataset, upload CSV test file (optional)",
                                                              type=["csv"], key='test')
                        st.write(" ")

                        submit_button = st.form_submit_button("AutoML")

                        if submit_button:
                            st.session_state.form_submitted = True


            # Process form submission and display download button
            if st.session_state.form_submitted and st.session_state.begin_clu and features:
                st.markdown('<p style="color:#4FFF33">Setup Successfully Completed!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                # st.write("Model created")
                model_id = model_df[model_df['Name'] == cluster_model].index[0]
                with st.spinner("Running......"):
                    if num_clusters >1:
                        created_model = create_model(model_id, num_clusters=num_clusters)
                    else:
                        created_model = create_model(model_id)
                st.write("#### ",cluster_model)
                st.write(pull())
                st.write("Assign")
                assigned_result = assign_model(created_model)
                st.dataframe(assigned_result)
                # save model
                save_model(created_model, 'clustering_model')

                # save_model(created_model, 'created_model')


                if len(selected_metrics) >= 1 and created_model:
                    tabs = st.tabs(selected_metrics)
                    for metric, tab in zip(selected_metrics, tabs):
                        with tab:
                            try:
                                img = plot_model(created_model, plot=metrics_dict[metric], display_format='streamlit',
                                                 save=True)
                                st.image(img)
                            except:
                                try:
                                    plot_model(created_model, plot=metrics_dict[metric], display_format='streamlit')
                                    # st.write(
                                        # "The plot is currently inaccessible in this window. However, you can view it in the newly opened window.")
                                except:
                                    st.write("The plot is unavailable; please consider using alternative evaluation metrics.")


                    try:
                        # Predicts label on the holdout set.
                        pred_holdout = predict_model(created_model, data_unseen)
                        st.write('#### Predictions from holdout set (validation set)')
                        st.dataframe(pred_holdout)
                    except Exception as e:
                        st.error(str(e))
                        # st.error("Something went wrong, please try other models")

                # else:
                    # st.warning("Choose the models")

                if uploaded_file_test:
                    st.write('### Test data')
                    test_dataset = pd.read_csv(uploaded_file_test)
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

            # Display download button if model is saved
            if st.session_state.model_saved:
                with open('clustering_model.pkl', 'rb') as f:
                    st.download_button(
                        label="Download Clustering Model",
                        data=f,
                        file_name='clustering_model.pkl',
                        mime='application/octet-stream'
                    )
