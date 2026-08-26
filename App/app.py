import streamlit as st
from chatbot import ask_chatbot

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------- COMPACT CHATBOT STYLE ----------

st.markdown("""
<style>

    /* Remove default Streamlit top spacing */
    .block-container {
        padding-top: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        max-width: 100%;
    }

    /* Main background */
    .stApp {
        background-color: #0B0F19;
    }

    /* Assistant title */
    .assistant-title {
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin-bottom: 4px;
    }

    .assistant-subtitle {
        font-size: 11px;
        color: #B8BEC9;
        margin-bottom: 12px;
    }

    /* Suggestion buttons */
    .stButton > button {
        width: 100%;
        background-color: #151B2A;
        color: #E5E7EB;
        border: 1px solid #252C43;
        border-radius: 7px;
        font-size: 10px;
        padding: 5px 4px;
        margin-bottom: 4px;
    }

    .stButton > button:hover {
        border-color: #14B8A6;
        color: white;
    }

    /* Chat input */
    .stChatInput {
        padding-bottom: 0;
    }

    .stChatInput > div {
        border: 1px solid #252C43 !important;
        border-radius: 8px !important;
        background-color: #151B2A !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        padding: 6px 4px;
    }

    /* Assistant response */
    .assistant-answer {
        background-color: #151B2A;
        border-left: 3px solid #14B8A6;
        padding: 8px 9px;
        border-radius: 6px;
        color: #F3F4F6;
        font-size: 11px;
        line-height: 1.4;
    }

</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------

st.markdown(
    '<div class="assistant-title">🤖 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="assistant-subtitle">Ask about your retail data</div>',
    unsafe_allow_html=True
)


# ---------- CHAT HISTORY ----------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------- QUICK QUESTIONS ----------

st.caption("Quick questions")

col1, col2 = st.columns(2)

with col1:

    if st.button("Highest revenue"):
        question = "Which country generated the highest revenue?"
        st.session_state.pending_question = question

with col2:

    if st.button("Top customer"):
        question = "Who is the top customer by revenue?"
        st.session_state.pending_question = question


col3, col4 = st.columns(2)

with col3:

    if st.button("Best product"):
        question = "Which product generated the highest revenue?"
        st.session_state.pending_question = question

with col4:

    if st.button("Best month"):
        question = "Which month generated the highest revenue?"
        st.session_state.pending_question = question


# ---------- CHAT INPUT ----------

question = st.chat_input(
    "Ask a business question..."
)


# Use quick-question selection if clicked
if "pending_question" in st.session_state:

    question = st.session_state.pending_question
    del st.session_state.pending_question


# ---------- PROCESS QUESTION ----------

if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Analyzing..."):

            result = ask_chatbot(question)


        if result["success"]:

            answer = result["answer"]

            st.markdown(
                f'<div class="assistant-answer">{answer}</div>',
                unsafe_allow_html=True
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        else:

            error_message = (
                "I couldn't process that question. "
                "Please try again."
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )