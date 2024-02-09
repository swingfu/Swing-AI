import streamlit as st
import openai


st.title("Try ChatGPT for tutoring! 🤖️ ") 

# set the endpoint and Appkey
openai.api_type = "azure"
openai.base_url = "https://ai4kidseus2-aiservices-1020859675.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-07-01-preview"
openai.api_version = "2023-07-01-preview"
openai_api_key = st.secrets['OPENAI_API_KEY']
openai.api_key = openai_api_key


# default message
if "messages" not in st.session_state: 
    st.session_state["messages"] = [{
        "role": "assistant",
        "content": "You are using ChatGPT-4 now, how can I help you?" 
    }]

# deal with the conversation 
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# deal exception with no credential
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

# accpet user prompt and create response 
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.chat.completions.create(model='gpt-4', messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)