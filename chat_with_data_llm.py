import streamlit as st
import os
import google.generativeai as genai
import pandas as pd
import json
import plotly.express as px
from pycaret.datasets import get_data

GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

def chatData():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Please provide the data to proceed.")
        return

    st.title("InsightBot")
    st.empty()
    st.markdown("###### InsightBot allows you to chat with your data "
                "using  [Google Gemini-1.5-Flash-Latest](https://deepmind.google/technologies/gemini/flash/). ")
    st.empty()

    if st.session_state.df is not None:
        df = st.session_state.df
        st.write("## Data Preview:")
        st.dataframe(df)

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hi , How can I help you?"}]
        elif "messages" in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])


        if user_query := st.chat_input():
            st.chat_message("user").write(user_query)
            system_instruction = f"Analyze this data: {df} \n\nQuestion: {user_query}"
            model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=system_instruction)
            prompt = (f"If the answer requires generating code, include it in the response. "
                        f"Format the code in a JSON object under the key 'code' and text response under the key 'answer' . For example, if the user asks to "
                        f"plot a bar chart for column A, the JSON output should include the necessary pandas code "
                        f"without print statements, like this: dict('code': 'pandas code here').If no code generated then return JSON object dict('answer': 'generated answer','code':''). Use Plotly for any "
                        f"visualizations and assign to fig and must display all figures in streamlit tabs no need to set set_page_config and sidebars. "
                        f"There is no need to include read data from a file as you already have the data as df."
                        f"make sure code will work")
            response = model.generate_content(prompt,
                                              generation_config=genai.GenerationConfig(
                                                  response_mime_type="application/json",
                                                  temperature=0.3,
                                              ),
                                              safety_settings={
                                                  'HATE': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'HARASSMENT': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'SEXUAL': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'DANGEROUS': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED'
                                              }
                                              )

            try:
                answer = json.loads(response.text)["answer"]
                code = json.loads(response.text)['code']
                if answer:
                    st.chat_message("assistant").write(answer)
                if code:
                    st.code(code)
                    try:
                        exec(code)
                    except:
                        st.empty()
                if not answer and not code:
                    try:
                        search_string = '{"answer": "'
                        start_index = response.text.find(search_string)

                        if start_index != -1:
                            # Extract the information after the search_string
                            result = response.text[start_index + len(search_string):]
                            st.chat_message("assistant").write(result)
                    except :
                        st.empty()
            except Exception as e:
                st.error(f"Sorry, no information was generated. Please try again or rephrase your question: {str(e)}")
                st.write(response.candidates[0].safety_ratings)

