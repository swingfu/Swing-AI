import streamlit as st

# main page for introduction of this program
st.title("Welcome to AI4Kids! 👋")

st.markdown(
    """
    AI4Kids is an innovative project aimed to explore the way to help children learning knowledge effectively based on the cutting-edge technology.
    **Select a model from the sidebar** to see the result of different answers from different LLMs!
    ### Want to learn more? 
    - Check out document for [chatGPT](https://chat.openai.com/)
    - Contact us to join the project

    ### See other projects from AI4Life
    - AI for Health
    - AI for eWorker

"""
)

# side bar options
st.sidebar.success("Select a model to test")

