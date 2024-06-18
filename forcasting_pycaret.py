import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pycaret.time_series import *
def timeseriesPycaret():
    st.subheader("AutoML - Time Series Forecasting")
    if 'begin' not in st.session_state:
        st.session_state.begin = False

    if not st.session_state.begin:
        st.info("To get started, double-click on the Begin button.")
        if st.button(" Begin "):
            st.session_state.begin = True
            st.session_state.button_clicked = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("To restart AutoML, click on the 'Reset' button.")
        if st.button("Reset"):
            st.session_state.begin = True
            st.session_state.button_clicked = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()

        dataset = st.session_state.df
        nav_option = None
        fig_kwargs = {
            # "renderer": "notebook",
            "renderer": "png",
            "width": 1000,
            "height": 400,
        }
        # Initialize session state variables
        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False
        if 'prediction_submitted' not in st.session_state:
            st.session_state.prediction_submitted = False
        if 'model_saved' not in st.session_state:
            st.session_state.model_saved = False


        if len(dataset) > 0:
            st.write("### Data Preview")
            st.write(dataset)
            with st.container(border=True):
                st.header("Dataset Configuration")
                # st.write(dataset.index.name)
                column_list = dataset.columns.to_list()
                column_list.append(dataset.index.name)
                col1, col2 = st.columns(2)
                date_column = col1.selectbox("Select the Date Column",column_list )
                column_list.remove(date_column)
                target_column = col2.selectbox("Select the Target Columns", column_list)
                # Adjust dataset based on the selected columns
                if date_column == dataset.index.name:
                    dataset[date_column] = dataset.index
                elif target_column == dataset.index.name:
                    dataset[target_column] = dataset.index
                # Prepare the dataset for modeling
                data_preped = dataset[[date_column,target_column]]
                data_preped.set_index(date_column)
                data_preped.drop(date_column, axis=1, inplace=True)
                # Additional configuration for modeling
                folds = col1.slider("Number of folds for cross-validation",2,20,1)
                fh = col2.slider("Forecasting horizon (fh)", 1,365,1)
                window_splitter = col1.selectbox("Select type of window splitter ", ['expanding','sliding','rolling'])
                seasonal_period = col2.slider("Choose the seasonal period",0,1000,1)
                if seasonal_period == 0:
                    seasonal_period = None
                tune_YN = st.checkbox("Do you need to tune the model")
                # Primary button
                if st.button('Submit'):
                    st.session_state.button_clicked = True
                # submit_button = st.button("Submit")
            if st.session_state.button_clicked:
                st.write("### Prepared Dataset")
                st.dataframe(data_preped)
                with st.spinner("Running......"):
                    try:
                        s = setup(data_preped, fh=fh, fold=folds, seasonal_period=seasonal_period,
                                  fold_strategy=window_splitter, fig_kwargs=fig_kwargs, session_id=123, verbose=False)
                        with (st.container(border=True)):
                            st.markdown('<p style="color:#4FFF33"> ### Setup Successfully Completed!</p>', unsafe_allow_html=True)
                            setup_df = pull()
                            st.write("#### ", setup_df.iloc[25][0], ":", setup_df.iloc[25][1])
                            col1, col2 = st.columns(2)
                            col1.dataframe(pull())
                            with col2:
                                plot_model(display_format='streamlit')
                            col1.write("### Check Stats")
                            col1.dataframe(check_stats())
                            col2.write('#### Comparing All Models')
                            best = compare_models()
                            models_df = pull()
                            save_model(best, "best_model")
                            st.session_state.model_saved = True
                            col2.dataframe(pull())
                    except Exception as e:
                        st.error(str(e))

                nav_option = option_menu(menu_title="Models", options=["Best model","Specific Model"], orientation='horizontal')
                # nav_option = st.selectbox("Select a model option",["Best model","Specific Model"])

                if nav_option == "Best model":
                    try:
                        with (st.container(border=True)):
                            st.write("### Best Model: ", models_df['Model'].iloc[0])

                            col1, col2 = st.columns(2)
                            with col1:
                                plot_model(plot="cv",display_format='streamlit')
                            if tune_YN:
                                best_tuned = tune_model(best)
                                save_model(best_tuned,"tuned_best_model")
                                models_created = [best,best_tuned]
                                data_kwargs = {"labels": ["Best", "Best Tuned"]}
                            else:
                                models_created = [best]
                                data_kwargs = {"labels": ["Best"]}
                            with col2:
                                # plot forecast
                                plot_model(models_created, plot='forecast', data_kwargs=data_kwargs, display_format='streamlit')
                            with col1:
                                plot_model(models_created, plot='diagnostics', data_kwargs=data_kwargs, display_format='streamlit')
                            with col2:
                                plot_model(models_created, plot='insample', data_kwargs=data_kwargs, display_format='streamlit')
                            with col1:
                                # residuals plot
                                plot_model(models_created, plot='residuals', data_kwargs=data_kwargs, display_format='streamlit')
                            if best_tuned:
                                # predict on test set
                                holdout_pred = predict_model(best_tuned)
                            with col2:
                                st.write('#### Predictions from holdout set (validation set)')
                                st.dataframe(holdout_pred)
                        prediction_period = st.number_input("Select the forecast period into the future", 0,365,1)
                        if prediction_period >0:
                            st.session_state.prediction_submitted = True
                    except ValueError as e:
                        st.error(str(e))

                elif nav_option == "Specific Model":
                    # model_df = models()
                    forcasting_model = st.selectbox("Choose the model name", models_df['Model'].to_list())
                    model_id = models_df[models_df['Model'] == forcasting_model].index[0]
                    try:
                        model = create_model(model_id)
                        with (st.container(border=True)):
                            st.write("### Model: ", forcasting_model)
                            save_model(model, "model")
                            st.session_state.model_saved = True
                            col1, col2 = st.columns(2)
                            col1.write("### ")
                            col1.dataframe(pull())

                            if tune_YN:
                                model_tuned = tune_model(model)
                                save_model(model_tuned, "tuned_model")
                                models_created = [model,model_tuned, best]
                                data_kwargs = {"labels": ["Model", "Model Tuned","Best"]}
                            else:
                                models_created = [model]
                                data_kwargs = {"labels": ["Model"]}
                            with col2:
                                # plot forecast
                                plot_model(models_created, plot='forecast', data_kwargs=data_kwargs, display_format='streamlit')
                            with col1:
                                plot_model(models_created, plot='diagnostics', data_kwargs=data_kwargs,
                                           display_format='streamlit')
                            with col2:
                                plot_model(models_created, plot='insample', data_kwargs=data_kwargs, display_format='streamlit')
                            with col1:
                                # residuals plot
                                plot_model(models_created, plot='residuals', data_kwargs=data_kwargs,
                                           display_format='streamlit')
                            # predict on test set
                            holdout_pred = predict_model(best)
                            with col2:
                                st.write('#### Predictions from holdout set (validation set)')
                                st.dataframe(holdout_pred)
                        prediction_period = st.number_input("Select the forecast period into the future", 0, 365, 1)
                        if prediction_period > 0:
                            st.session_state.prediction_submitted = True
                    except ValueError as e:
                        st.error(str(e))
                    except:
                        st.write("Something wrong, Please try other models")


            if st.session_state.prediction_submitted > 0:
                st.write('#### Predictions: Forecasting horizon : ', prediction_period)
                st.dataframe(predict_model(best, fh=prediction_period, return_pred_int=True))
                # plot forecast for fh months in future
                plot_model(models_created, plot='forecast', data_kwargs={'fh': prediction_period}, display_format='streamlit')
            # Display download button if model is saved
            if st.session_state.model_saved:
                with open('best_model.pkl', 'rb') as f:
                    st.download_button(
                        label="Download Best Model",
                        data=f,
                        file_name='best_model.pkl',
                        mime='application/octet-stream'
                    )
                if nav_option == "Best model" and tune_YN :
                    with open('tuned_best_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Tuned Best Model",
                            data=f,
                            file_name='tuned_best_model.pkl',
                            mime='application/octet-stream'
                        )
                if nav_option == "Specific Model":
                    with open('model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Model",
                            data=f,
                            file_name='model.pkl',
                            mime='application/octet-stream'
                        )
                if nav_option == "Specific Model" and tune_YN :
                    with open('tuned_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Download Tuned Model",
                            data=f,
                            file_name='tuned_model.pkl',
                            mime='application/octet-stream'
                        )

        else:
            st.write("Please upload a data file.")
