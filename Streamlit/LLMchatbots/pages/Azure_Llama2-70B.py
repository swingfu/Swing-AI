import urllib.request
import json
import os
import ssl
import streamlit as st

st.title("Try Llama2-70B for tutoring! 🦙 ") 

# Set the Azure API token 
with st.sidebar:
    st.write('This chatbot is created using the open-source Llama2-70b, using the API hosted on Azure AI platform')
    if 'AZURE_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        azure_api = os.getenv('AZURE_API_KEY')
    else:
        azure_api = st.text_input('Enter Replicate API token:', key="llama_replicate_key", type='password')
        if not (azure_api.startswith('r8_') and len(azure_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['AZURE_API_KEY'] = azure_api

    st.subheader('Model parameters')
    temperature = st.sidebar.slider('temperature',0.01,5.0,0.1,0.01)
    top_p = st.sidebar.slider('top_p',0.01,1.0,0.9,0.01)

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# default message
if "messages1" not in st.session_state: 
    st.session_state["messages1"] = [{
        "role": "assistant",
        "content": "You are using Llama2 now, how can I help you?" 
    }]

# deal with the conversation 
for msg in st.session_state.messages1:
    st.chat_message(msg["role"]).write(msg["content"])

# deal exception with no credential
if prompt := st.chat_input():
    if not azure_api:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages1.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    data = {"messages":[
    {
        "role":"user",
        "content": prompt,
    }
],
        "temperature":temperature, "top_p":top_p}
    body = str.encode(json.dumps(data))
    url = 'https://Llama-2-70b-chat-urdfk-serverless.eastus2.inference.ai.azure.com/v1/chat/completions'
    if not azure_api:
      raise Exception("A key should be provided to invoke the endpoint")
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ azure_api)}
    req = urllib.request.Request(url, body, headers)
    response = urllib.request.urlopen(req)
    result = response.read()
    jsonResponse = json.loads(result.decode('utf-8'))
    k1 = jsonResponse['choices'][0]
    msg = k1['message']['content']
    st.session_state.messages1.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    