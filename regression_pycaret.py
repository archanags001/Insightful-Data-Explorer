import streamlit as st
import pandas as pd
from pycaret.regression import setup, compare_models, predict_model, pull, plot_model, create_model, ensemble_model, blend_models, stack_models, tune_model, save_model




# Dictionary of metrics
metrics_dict_reg = {
    "Residuals Plot": 'residuals',
    "Prediction Error Plot": 'error',
    "Cooks Distance Plot": 'cooks',
    "Recursive Feature Selection": 'rfe',
    "Learning Curve": 'learning',
    "Validation Curve": 'vc',
    "Manifold Learning": 'manifold',
    "Feature Importance (Top 10)": 'feature',
    "Feature IImportance (all)": 'feature_all',

}

def regressionPycaret():
    st.subheader("AutoML - Regression")
    if 'begin_reg' not in st.session_state:
        st.session_state.begin_reg = False

    if not st.session_state.begin_reg:
        st.info("To get started, double-click on the Begin button.")
        if st.button("Begin"):
            st.session_state.begin_reg = True
            st.session_state.button_clicked_reg = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("To restart AutoML, click on the 'Reset' button.")
        if st.button("Reset"):
            st.session_state.begin_reg = True
            st.session_state.button_clicked_reg = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()
        dataset = st.session_state.df
        option_reg = None
        model_reg = None
        uploaded_file_test_reg = None
        tune_YN_reg = None
        final_model_reg = None

        if len(dataset) > 0:

            st.write("### Data Preview")
            st.write(dataset)
            st.header("Dataset Configuration")

            col1,col2 = st.columns(2)
            # col1.header('Select Target Column')
            target_reg = col1.selectbox("Choose the target column:", dataset.columns, index=None,
                            placeholder="Select the target column...")
            if target_reg:
                feature_list_reg = dataset.columns.tolist()
                feature_list_reg.remove(target_reg)
                # col2.header('Select Features')
                features_reg = col2.multiselect("Select features to include:", feature_list_reg)

                train_size = col1.slider("Set the training data size:", 0.1, 0.9, 0.8)
                validation_size = col2.slider("Set the validation data size:", 0.1, 0.9 - train_size, 0.1)
                test_size = 1 - train_size - validation_size
                features_reg.append(target_reg)
                data_reg = dataset[features_reg].sample(frac=train_size, random_state=786).reset_index(drop=True)
                data_unseen_reg = dataset[features_reg].drop(data_reg.index).reset_index(drop=True)

                if "button_clicked_reg" not in st.session_state:
                    st.session_state.button_clicked_reg = False
                if 'form_submitted' not in st.session_state:
                    st.session_state.form_submitted = False
                if 'model_saved' not in st.session_state:
                    st.session_state.model_saved = False
                # submit_button_reg = False

                # Outer button
                outer_button_clicked_reg = st.button("Submit")

                if outer_button_clicked_reg:
                    if len(features_reg) <= 1:  # Since we always include the target, check if more than 1 feature is selected
                        st.warning("Select features to include:")
                    else:
                        st.session_state.button_clicked_reg = True

            else:
                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_reg = False
                else:
                    st.session_state.button_clicked_reg = False


            if st.session_state.button_clicked_reg :
                # with st.spinner("Running......"):
                try:
                    s_reg = setup(data_reg, target=target_reg, session_id=123)
                except Exception as e:
                    st.error(str(e))
                st.markdown('<p style="color:#4FFF33">Setup Successfully Completed!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                with st.spinner("Running......"):
                    # get best model
                    best_reg = compare_models()
                    # get the scoring grid
                    results_reg = pull()
                    try:
                        st.write("### Best Model: ", results_reg['Model'].iloc[0])
                    except Exception as e:
                        st.error("Something appears to be incorrect. Please ensure that your target columns and features "
                                     "are selected correctly. If you encounter any further issues, feel free to reach out. "
                                     "Contact information can be found on the 'About' page.")
                    # st.write("### Best Model: ", results_reg['Model'].iloc[0])
                    st.write('#### Comparing All Models')
                    model_df_reg = st.dataframe(pull())

                # # Get the name of the best model
                # model_name_reg = None
                # tune_YN_reg = None
                st.write("### Model Selection and Configuration")
                with st.form(key='model_form_reg'):
                    option_reg = st.selectbox("Select a model option",
                                              ["Best Model", "Specific Model", "Ensemble Model", "Blending", "Stacking"])
                    st.markdown('<p style="color:#3355FF">Please choose a model option and click the button below to confirm '
                                'your selection before filling out the other fields.</p>',unsafe_allow_html=True)



                    change_reg = st.form_submit_button("Click here to confirm the model selection")
                    model_name_reg = None
                    if option_reg == "Specific Model":
                        model_name_reg = st.selectbox("Choose the model name", results_reg['Model'].to_list())
                    elif option_reg == "Ensemble Model":
                        model_name_reg = st.selectbox("Choose the model to ensemble", results_reg['Model'].to_list())
                        method_reg = st.selectbox("Choose the ensemble method: ",['Bagging','Boosting'])
                    elif option_reg == "Blending":
                        blend_models_list = st.multiselect("Choose the models for blending", results_reg['Model'].to_list())
                        # method = st.selectbox("Choose blending method: ",['soft','hard'])
                    elif option_reg == "Stacking":
                        stack_models_list_reg = st.multiselect("Choose models for stacking", results_reg['Model'].to_list())

                    tune_YN_reg = st.checkbox ("Do you need to tune the model")

                    selected_metrics_reg = st.multiselect("Select regression metrics to evaluate",options=list(metrics_dict_reg.keys()))
                    uploaded_file_test_reg = st.file_uploader("If you want to upload a test dataset,Upload CSV or Excel test file (optional)",
                                                          type=["csv", "xlsx"], key='test')

                    submit_button_reg = st.form_submit_button(label='Run AutoML')
                    if submit_button_reg:
                        st.session_state.form_submitted = True


                # except ValueError as e:
                #     st.write(str(e))


            # Display the selected items if the form is submitted
            if st.session_state.form_submitted and st.session_state.begin_reg:
                st.write("You have selected the model:",option_reg)

                if option_reg == "Best Model":
                    model_reg = best_reg
                    model_name_reg = results_reg['Model'].iloc[0]
                    save_model(best_reg,"best")

                elif option_reg == "Specific Model":
                    m_name_reg = results_reg[results_reg['Model'] == model_name_reg].index[0]
                    model_reg = create_model(m_name_reg)
                    st.write("#### model: ", model_name_reg)
                    st.dataframe(pull())
                    save_model(model_reg,"specific_model")

                elif option_reg == "Ensemble Model":
                    if model_name_reg is not None:
                        m_name_reg = results_reg[results_reg['Model'] == model_name_reg].index[0]
                        model_reg = create_model(m_name_reg)
                        model_reg = ensemble_model(model_reg, method =method_reg)
                        st.write("#### model: ", model_name_reg, "method: ", method_reg)
                        st.dataframe(pull())
                        save_model(model_reg, "ensemble_model")
                    else:
                        st.warning("Choose the models for ensemble")

                elif option_reg == "Blending":
                    if blend_models_list is not None:
                        model_list_reg = []
                        blend_models_name_reg = "Blending: "
                        for i in blend_models_list:
                            m_name_reg = results_reg[results_reg['Model'] == i].index[0]
                            model_list_reg.append(create_model(m_name_reg, verbose=False))
                            blend_models_name_reg = blend_models_name_reg+", "+i
                        model_name_reg = blend_models_name_reg
                        try:
                            model_reg = blend_models(estimator_list=model_list_reg)
                            save_model(model_reg, "blending_model")

                        except TypeError as e:
                            st.error(str(e))
                            st.error("Please try other models")
                        except:
                            st.write("Something wrong, Please try other models")
                    else:
                        st.warning("Choose the models for blending")

                elif option_reg == "Stacking":
                    if stack_models_list_reg is not None:
                        model_list_reg = []
                        stacking_models_reg = "Stacking: "
                        for i in stack_models_list_reg:
                            m_name_reg = results_reg[results_reg['Model'] == i].index[0]
                            model_list_reg.append(create_model(m_name_reg, verbose=False))
                            stacking_models_reg = stacking_models_reg+", "+i
                        model_name_reg = stacking_models_reg

                        try:
                            model_reg = stack_models(model_list_reg)
                            save_model(model_reg, "stacking_model")
                        except TypeError as e:
                            st.error(str(e))
                            st.error("Please try other models")
                        except:
                            st.write("Something wrong, Please try other models")
                    else:
                        st.warning("Choose the models for stacking")

                if model_reg:
                    if tune_YN_reg:
                        try:
                            final_model_reg = tune_model(model_reg)
                            st.write("#### Tuned Model: ", model_name_reg)
                            st.dataframe(pull())
                            save_model(final_model_reg, "tuned_model")
                        except Exception as e:

                            st.error(str(e))
                            st.info("Please try other models")
                        except:
                            st.write("Something wrong, Please try other models")

                    else:
                        final_model_reg = model_reg

                    if len(selected_metrics_reg) >= 1 and final_model_reg :
                        tabs_reg = st.tabs(selected_metrics_reg)

                        for metric, tab in zip(selected_metrics_reg, tabs_reg):
                            with tab:
                                try:
                                    img = plot_model(final_model_reg, plot=metrics_dict_reg[metric], display_format='streamlit', save=True)
                                    st.image(img)
                                except:
                                    try:
                                        plot_model(final_model_reg, plot=metrics_dict_reg[metric], display_format='streamlit')
                                        # st.write(
                                        # "The plot is currently inaccessible in this window. However, you can view it in the newly opened window.")
                                    except:
                                        st.write( "The plot is unavailable; please consider using alternative evaluation metrics.")
                                    # st.write("The plot is unavailable; please consider using alternative evaluation metrics.")
                    try:
                        # Predicts label on the holdout set.
                        pred_holdout_reg = predict_model(final_model_reg)
                        st.write('#### Predictions from holdout set(validation set)')
                        st.dataframe(pred_holdout_reg)
                    except Exception as e:
                        st.error(str(e))

                else:
                    st.warning("Choose the models")
                st.session_state.model_saved = True

                if uploaded_file_test_reg and final_model_reg:
                    st.write('### Test data')
                    # test_dataset_reg = pd.read_csv(uploaded_file_test_reg)
                    # st.dataframe(test_dataset_reg)
                    if uploaded_file_test_reg.name.endswith('.csv'):
                        test_dataset_reg = pd.read_csv(uploaded_file_test_reg)
                    elif uploaded_file_test_reg.name.endswith(('.xlsx', '.xls')):
                        test_dataset_reg = pd.read_excel(uploaded_file_test_reg)
                    st.write("Test Data Preview:")
                    st.dataframe(test_dataset_reg)

                    try:

                        if target_reg in test_dataset_reg.columns:
                            # st.write(test_dataset.columns)
                            test_dataset_reg = test_dataset_reg[features_reg]
                            test_dataset_reg = test_dataset_reg.drop(target_reg, axis=1)
                            test_pred_reg = predict_model(final_model_reg, test_dataset_reg)
                            st.write("### Prediction")
                            st.dataframe(test_pred_reg)
                        else:
                            # st.write(test_dataset.columns)
                            features_reg.pop()
                            test_dataset = test_dataset_reg[features_reg]
                            # st.dataframe(test_dataset)
                            test_pred = predict_model(best_reg, test_dataset)
                            st.write("### Prediction")
                            st.dataframe(test_pred)
                    except Exception as e:
                        st.error(str(e))
                    # except:
                    #     st.error("Something wrong, Please try other models")

            # Display download button if model is saved
            if st.session_state.model_saved:
                if option_reg == "Best Model":
                    with open('best.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Best Model",
                            data=f,
                            file_name='best_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Specific Model":
                    with open('specific_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Specific Model",
                            data=f,
                            file_name='specific_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Ensemble Model":
                    with open('ensemble_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Ensemble Model",
                            data=f,
                            file_name='ensemble_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Blending":
                    with open('blending_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Blending Model",
                            data=f,
                            file_name='blending_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Stacking":
                    with open('stacking_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Stacking Model",
                            data=f,
                            file_name='stacking_model.pkl',
                            mime='application/octet-stream'
                        )
                if tune_YN_reg:
                    with open('tuned_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Tuned Model",
                            data=f,
                            file_name='tuned_model.pkl',
                            mime='application/octet-stream'
                        )

        else:
            st.write("Please upload a data file.")
