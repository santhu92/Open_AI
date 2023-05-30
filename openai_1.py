import streamlit as st
from app import api_key, Serpa_api
import subprocess
import os
def install_libraries():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        return print("Library installation successful!")
    except subprocess.CalledProcessError as e:
        return print("An error occurred while installing libraries:", e)

# Call the install_libraries() function to install the libraries
install_libraries()
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
import json
st.write(api_key)
os.environ['OPENAI_API_KEY'] = api_key
os.environ['SERPAPI_API_KEY'] = Serpa_api
SERPAPI_API_KEY = Serpa_api

openai_api_key = api_key
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []



def clear_text_input():
    global input_text
    input_text = ""

def get_text():
    global input_text
    input_text = st.text_input("Please ask me your question", on_change=clear_text_input)
    return input_text

def get_file(file_data):
    if '.csv' in file_data.name:
        df = pd.read_csv(file_data)
    elif '.json' in file_data.name:
        df = pd.read_json(file_data)
    else:
        df = pd.read_excel(file_data)
    return df
#create a file uploader
uploaded_file = st.file_uploader("choose a file")
user_input = get_text()
if uploaded_file:
    dataframe = get_file(uploaded_file)
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dataframe, verbose=True)

if st.button("Post"):
    with st.spinner("waiting for the response"):
        if user_input:
            output = agent.run(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')












