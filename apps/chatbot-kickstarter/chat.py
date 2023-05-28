import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

# System prompt requiring Question and Year to be extracted from the user
system_prompt = '''
You are a helpful Medicare Home Health knowledge base assistant. You need to capture a Question and any clarification information.
The Question is their query on Medicare Home Health Regulations, and the clarification information is any additional information they provide to help you answer their question.
If you need to ask the user for clarification information, ask them for it.
Once you have a Question and any clarification information, say "searching for answers".

Example 1:

User: I'd like to know if a clinician can perform a home health initial assessment.

Assistant: Certainly, which clinician did you want to know this about?

User: Physical Therapist, please.

Assistant: Searching for answers.
'''

### CHATBOT APP

st.set_page_config(
    page_title="Home Health Regs Chat - Demo",
    page_icon=":speech-ballon:"
)

st.title('Medicare Home Health Regulations Chatbot')
st.subheader("Help us help you learn about Medicare Home Health Regulations")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input(f"What do you want to know: ", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []


    user_message = Message('user',prompt)
    messages.append(user_message.message())

    response = query(messages)

    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
