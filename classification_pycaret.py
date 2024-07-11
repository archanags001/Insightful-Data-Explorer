import streamlit as st
import pandas as pd
from pycaret.classification import setup, compare_models, predict_model, pull, plot_model,create_model,ensemble_model,blend_models,stack_models,tune_model,save_model




# Dictionary of metrics
metrics_dict = {
    "Area Under the Curve": 'auc',
    "Discrimination Threshold": 'threshold',
    "Precision-Recall Curve": 'pr',
    "Confusion Matrix": 'confusion_matrix',
    "Class Prediction Error": 'error',
    "Classification Report": 'class_report',
    "Decision Boundary": 'boundary',
    "Recursive Feature Selection": 'rfe',
    "Learning Curve": 'learning',
    "Manifold Learning": 'manifold',
    "Calibration Curve": 'calibration',
    "Validation Curve": 'vc',
    "Dimension Learning": 'dimension',
    "Feature Importance (Top 10)": 'feature',
    "Feature IImportance (all)": 'feature_all',
    "Lift Curve":'lift',
    "Gain Curve": 'gain',
    "KS Statistic Plot":  'ks'
}
fig_kwargs = {
                    "renderer": "png",
                    "width": 1000,
                    "height": 400,
                }


def classificationPycaret():
    st.subheader("AutoML - Classification")
    if 'begin_cls' not in st.session_state:
        st.session_state.begin_cls = False

    if not st.session_state.begin_cls:
        st.info("To get started, double-click on the Begin button.")
        if st.button(" Begin "):
            st.session_state.begin_cls = True
            st.session_state.button_clicked_cls = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("To restart AutoML, click on the 'Reset' button.")
        if st.button("Reset"):
            st.session_state.begin_cls = True
            st.session_state.button_clicked_cls = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()
        dataset = st.session_state.df
        option = None
        model_cls = None
        uploaded_file_test = None
        tune_YN = None

        if len(dataset) > 0:
            st.write("### Data Preview")
            st.write(dataset)
            st.header("Dataset Configuration")

            col1,col2 = st.columns(2)
            # col1.header('Select Target Column')
            target = col1.selectbox("Choose the target column:", dataset.columns, index=None,
                        placeholder="Select the target column...")
            if target:
                feature_list = dataset.columns.tolist()
                feature_list.remove(target)
                features = col2.multiselect("Select features to include:", feature_list)
                train_size = col1.slider("Set the training data size:", 0.1, 0.9, 0.8)
                validation_size = col2.slider("Set the validation data size:", 0.1, 0.9 - train_size, 0.1)
                test_size = 1 - train_size - validation_size
                features.append(target)
                data = dataset[features].sample(frac=train_size, random_state=786).reset_index(drop=True)
                data_unseen = dataset[features].drop(data.index).reset_index(drop=True)
                results = pd.DataFrame()

                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_cls = False
                if 'form_submitted' not in st.session_state:
                    st.session_state.form_submitted = False
                if 'model_saved' not in st.session_state:
                    st.session_state.model_saved = False

                # Outer button
                outer_button_clicked_cls = st.button("Submit")


                if outer_button_clicked_cls:
                    # st.write(len(features))
                    if len(features) < 2:  # Since we always include the target, check if more than 1 feature is selected
                        st.warning("Select features to include:")
                        st.session_state.button_clicked_cls = False
                    else:
                        st.session_state.button_clicked_cls = True

            else:
                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_cls = False
                else:
                    st.session_state.button_clicked_cls = False

            if st.session_state.button_clicked_cls:
                try:
                    s = setup(data, target=target, session_id=123)
                except Exception as e:
                    st.error(str(e))
                st.markdown('<p style="color:#4FFF33">Setup Successfully Completed!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                # get best model
                best = compare_models()
                # get the scoring grid
                results = pull()
                st.write("### Best Model: ", results['Model'].iloc[0])
                st.write('#### Comparing All Models')
                model_df = st.dataframe(pull())
                # # Get the name of the best model
                model_name = None
                tune_YN = None
                st.write("### Model Selection and Configuration")
                with st.form(key='model_form'):
                    option = st.selectbox("Select a model option",
                                              ["Best Model", "Specific Model", "Ensemble Model", "Blending", "Stacking"])
                    st.markdown('<p style="color:#3355FF">Please choose a model option and click the button below to confirm '
                                'your selection before filling out the other fields.</p>',unsafe_allow_html=True)

                    change = st.form_submit_button("Click here to confirm the model selection")
                    if change:
                        st.session_state.form_submitted = False
                        st.session_state.model_saved = False

                    if option == "Specific Model":
                        model_name = st.selectbox("Choose the model name", results['Model'].to_list())
                    elif option == "Ensemble Model":
                        model_name = st.selectbox("Choose the model to ensemble", results['Model'].to_list())
                        method = st.selectbox("Choose the ensemble method: ",['Bagging','Boosting'])
                    elif option == "Blending":
                        blend_models_list = st.multiselect("Choose the models for blending", results['Model'].to_list())
                        method = st.selectbox("Choose blending method: ",['soft','hard'])
                    elif option == "Stacking":
                        stack_models_list = st.multiselect("Choose models for stacking", results['Model'].to_list())

                    tune_YN = st.checkbox ("Do you need to tune the model")

                    selected_metrics = st.multiselect("Select classification metrics to evaluate",options=list(metrics_dict.keys()))
                    uploaded_file_test = st.file_uploader("If you want to upload a test dataset,Upload CSV or Excel test file (optional)",
                                                          type=["csv", "xlsx"], key='test')

                    submit_button = st.form_submit_button(label='Run AutoML')
                    if submit_button:
                        st.session_state.form_submitted = True


            # Display the selected items if the form is submitted
            if st.session_state.form_submitted and st.session_state.begin_cls:
                st.write("You have selected the model:",option)

                if option == "Best Model":
                    model_cls = best
                    model_name = results['Model'].iloc[0]
                    save_model(model_cls, "best")

                elif option == "Specific Model":
                    m_name = results[results['Model'] == model_name].index[0]
                    model_cls = create_model(m_name)
                    st.write("#### model: ", model_name)
                    st.dataframe(pull())
                    save_model(model_cls,"specific_model")

                elif option == "Ensemble Model":
                    if model_name is not None:
                        m_name = results[results['Model'] == model_name].index[0]
                        try:
                            model_cls = create_model(m_name)
                            model = ensemble_model(model_cls, method =method)
                        except TypeError as e:
                            st.error(str(e))
                        st.write("#### model: ", model_name, "method: ", method)
                        st.dataframe(pull())
                        save_model(model, "ensemble_model")

                    else:
                        st.warning("Choose the models for ensemble")

                elif option == "Blending":
                    if blend_models_list is not None:
                        model_list = []
                        blend_models_name= "Blending: "
                        for i in blend_models_list:
                            m_name = results[results['Model'] == i].index[0]
                            model_list.append(create_model(m_name, verbose=False))
                            blend_models_name = blend_models_name+", "+i
                        model_name = blend_models_name
                        try:
                            model_cls = blend_models(estimator_list=model_list, method=method)
                            save_model(model_cls, "blending_model")
                        except TypeError as e:
                            st.error(f"Error: {e}")
                        except:
                            st.write("Something wrong, Please try other models")
                    else:
                        st.warning("Choose the models for blending")

                elif option == "Stacking":
                    if stack_models_list is not None:
                        model_list = []
                        stacking_models = "Stacking: "
                        for i in stack_models_list:
                            m_name = results[results['Model'] == i].index[0]
                            model_list.append(create_model(m_name, verbose=False))
                            stacking_models = stacking_models+", "+i
                        model_name = stacking_models

                        try:
                            model_cls = stack_models(model_list)
                            save_model(model_cls, "stacking_model")
                        except TypeError as e:
                            st.write(f"Error: {e}")
                        except:
                            st.write("Something wrong, Please try other models")
                    else:
                        st.warning("Choose the models for stacking")
                st.session_state.model_saved = True

                if model_cls:
                    if tune_YN:
                        try:

                            final_model = tune_model(model_cls)
                            save_model(final_model, "tuned_model")
                            st.write("#### Tuned Model: ", model_name)
                            st.dataframe(pull())
                        except TypeError as e:
                            st.write("Error: ", str(e))
                        except:
                            st.write("Something wrong, Please try other models")
                    else:
                        final_model = model_cls

                    if len(selected_metrics) >= 1 :
                        tabs = st.tabs(selected_metrics)

                        for metric, tab in zip(selected_metrics, tabs):
                            with tab:
                                try:
                                    img = plot_model(final_model, plot=metrics_dict[metric], display_format='streamlit', save=True)
                                    st.image(img)
                                except:
                                    try:
                                        plot_model(final_model, plot=metrics_dict[metric], display_format='streamlit')
                                        # st.write(
                                        # "The plot is currently inaccessible in this window. However, you can view it in the newly opened window.")
                                    except:
                                        st.write( "The plot is unavailable; please consider using alternative evaluation metrics.")
                                    # st.write("The plot is unavailable; please consider using alternative evaluation metrics.")
                    try:
                        # Predicts label on the holdout set.
                        pred_holdout = predict_model(final_model)
                        st.write('#### Predictions from holdout set(validation set)')
                        st.dataframe(pred_holdout)
                    except:
                        st.error("Something wrong, Please try other models")
                else:
                    st.warning("Choose the models")

                if uploaded_file_test:
                    st.write('### Test data')
                    if uploaded_file_test.name.endswith('.csv'):
                        test_dataset = pd.read_csv(uploaded_file_test)
                    elif uploaded_file_test.name.endswith(('.xlsx', '.xls')):
                        test_dataset = pd.read_excel(uploaded_file_test)
                    st.write("Test Data Preview:")
                    st.dataframe(test_dataset)
                    # test_dataset = pd.read_csv(uploaded_file_test)
                    # st.dataframe(test_dataset)
                    # st.write("### Prediction")
                    try:
                        if target in test_dataset.columns:
                            # st.write(test_dataset.columns)
                            test_dataset = test_dataset[features]
                            test_dataset = test_dataset.drop(target, axis=1)
                            test_pred = predict_model(final_model, test_dataset)
                            st.write("### Prediction")
                            st.dataframe(test_pred)
                        else:
                            # st.write(test_dataset.columns)
                            features.pop()
                            test_dataset = test_dataset[features]
                            # st.dataframe(test_dataset)
                            test_pred = predict_model(best, test_dataset)
                            st.write("### Prediction")
                            st.dataframe(test_pred)
                    except KeyError as e:
                        st.error(str(e))
                    except:
                        st.error("Something wrong, Please try other models")
            # Display download button if model is saved
            if st.session_state.model_saved:
                if option == "Best Model":
                    with open('best.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Best Model",
                            data=f,
                            file_name='best_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Specific Model":
                    with open('specific_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Specific Model",
                            data=f,
                            file_name='specific_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Ensemble Model":
                    with open('ensemble_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Ensemble Model",
                            data=f,
                            file_name='ensemble_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Blending":
                    with open('blending_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Blending Model",
                            data=f,
                            file_name='blending_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Stacking":
                    with open('stacking_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Stacking Model",
                            data=f,
                            file_name='stacking_model.pkl',
                            mime='application/octet-stream'
                        )
                if tune_YN:
                    with open('tuned_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Tuned Model",
                            data=f,
                            file_name='tuned_model.pkl',
                            mime='application/octet-stream'
                        )




        else:
            st.write("Please upload a data file.")
