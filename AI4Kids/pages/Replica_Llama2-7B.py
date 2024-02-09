import streamlit as st
import os
import replicate


st.title("Try Llama2 for tutoring! 🦙 ") 

# Set the Replicate API token 
with st.sidebar:
    st.write('This chatbot is created using the open-source Llama2-7b/13b, using the API hosted on Replicate platform')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', key="llama_replicate_key", type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Model parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model',['Llama2-7B','Llama2- 13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

    temperature = st.sidebar.slider('temperature',0.01,5.0,0.1,0.01)
    top_p = st.sidebar.slider('top_p',0.01,1.0,0.9,0.01)

# Default message
if "messages2" not in st.session_state.keys():
    st.session_state.messages2 = [{"role": "assistant", "content": "You are using Llama2 now, how can I help you?"}]

# Deal with the conversation
for message in st.session_state.messages2:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# accept user prompt input
if prompt := st.chat_input(disabled = not replicate_api):
    st.session_state.messages2.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# function for generate response.
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages2:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "repetition_penalty":1})
    return output

# Generate a new response if last message is not from assistant
if st.session_state.messages2[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages2.append(message)