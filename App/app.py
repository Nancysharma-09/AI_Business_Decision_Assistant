import streamlit as st
from chatbot import ask_chatbot


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Business Decision Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM DASHBOARD + AI THEME
# =========================================================

st.markdown("""
<style>

    /* =====================================================
       MAIN APPLICATION
       ===================================================== */

    .stApp {
        background: #0B0F19;
    }

    .block-container {
        max-width: 900px;
        padding: 1.2rem 1.5rem 5rem 1.5rem;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .ai-header {
        position: relative;

        background: linear-gradient(
            135deg,
            #111827 0%,
            #151B2A 55%,
            #101624 100%
        );

        border: 1px solid #252C43;
        border-radius: 14px;

        padding: 22px 24px;
        margin-bottom: 20px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255,255,255,0.02);

        overflow: hidden;
    }

    .ai-header::after {
        content: "";
        position: absolute;

        width: 160px;
        height: 160px;

        right: -70px;
        top: -80px;

        background: rgba(239, 68, 68, 0.08);
        border-radius: 50%;

        pointer-events: none;
    }

    .ai-brand {
        color: #EF4444;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }

    .ai-title {
        color: #FFFFFF;
        font-size: 25px;
        font-weight: 700;
        line-height: 1.2;
        margin: 0;
    }

    .ai-subtitle {
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 8px;
    }

    .ai-status {
        display: inline-block;

        margin-top: 13px;
        padding: 4px 9px;

        background: rgba(239, 68, 68, 0.08);

        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 20px;

        color: #FCA5A5;

        font-size: 9px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        color: #9CA3AF;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;

        margin: 15px 0 8px 2px;
    }


    /* =====================================================
       QUICK INSIGHT BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100%;

        min-height: 44px;

        background: #111827;
        color: #E5E7EB;

        border: 1px solid #252C43;
        border-radius: 9px;

        font-size: 11px;
        font-weight: 600;

        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        background: #171D2D;
        color: #FFFFFF;

        border-color: #EF4444;

        transform: translateY(-1px);

        box-shadow:
            0 5px 15px rgba(239, 68, 68, 0.10);
    }


    /* =====================================================
       CHAT AREA
       ===================================================== */

    [data-testid="stChatMessage"] {
        background: transparent;
        padding: 8px 2px;
        margin-bottom: 5px;
    }

    [data-testid="stChatMessage"] p {
        color: #E5E7EB;
        font-size: 13px;
        line-height: 1.55;
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    .stChatInput {
        padding-bottom: 0;
    }

    .stChatInput > div {
        background: #111827 !important;

        border: 1px solid #252C43 !important;
        border-radius: 11px !important;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20) !important;
    }

    .stChatInput > div:focus-within {
        border-color: #EF4444 !important;

        box-shadow:
            0 0 0 1px #EF4444,
            0 8px 25px rgba(0, 0, 0, 0.25) !important;
    }


   /* =====================================================
   AI INSIGHT
   ===================================================== */

.assistant-label {
    display: inline-block;

    color: #EF4444;
    background: rgba(239, 68, 68, 0.08);

    border: 1px solid rgba(239, 68, 68, 0.22);
    border-radius: 20px;

    padding: 4px 9px;
    margin: 4px 0 8px 2px;

    font-size: 9px;
    font-weight: 700;

    letter-spacing: 1.2px;
    text-transform: uppercase;
}


/* =====================================================
   AI RESPONSE AREA
   ===================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #101624;

    border: 1px solid #252C43;
    border-left: 3px solid #EF4444;

    border-radius: 12px;

    padding: 12px 14px;

    margin: 6px 0 12px 0;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.16);
}


/* AI response text */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) p {
    color: #E5E7EB;

    font-size: 13px;
    line-height: 1.6;
}


/* Bold information */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) strong {
    color: #FFFFFF;
    font-weight: 700;
}


/* Headings inside AI response */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) h1,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) h2,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) h3 {
    color: #FFFFFF;

    margin-top: 5px;
    margin-bottom: 8px;
}


/* =====================================================
   AI TABLE
   ===================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) table {
    width: 100%;

    background: #0B0F19;

    border: 1px solid #252C43;

    border-radius: 8px;

    overflow: hidden;

    font-size: 12px;
}


/* Table header */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) th {
    background: #151B2A;

    color: #FFFFFF;

    font-weight: 700;

    border-bottom: 1px solid #252C43;
}


/* Table cells */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) td {
    color: #D1D5DB;

    border-bottom: 1px solid #1D2435;
}


/* Last row */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) tr:last-child td {
    border-bottom: none;
}


/* =====================================================
   DIVIDER
   ===================================================== */

.soft-divider {
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        #252C43,
        transparent
    );

    margin: 18px 0;
}

    /* =====================================================
       CLEAR CHAT BUTTON
       ===================================================== */

    .clear-button > button {
        min-height: 30px !important;

        background: transparent !important;

        border: 1px solid #252C43 !important;

        color: #6B7280 !important;

        font-size: 9px !important;
    }

    .clear-button > button:hover {
        color: #EF4444 !important;
        border-color: #EF4444 !important;
    }


    /* =====================================================
       SPINNER
       ===================================================== */

    .stSpinner > div {
        border-top-color: #EF4444 !important;
    }


    /* =====================================================
       HIDE STREAMLIT BRANDING
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

# ---------- HEADER ----------

st.markdown("""
<div class="ai-header">
<div class="ai-brand">◈ AI BUSINESS INTELLIGENCE</div>
<div class="ai-title">AI Business Decision Assistant</div>
<div class="ai-subtitle">Ask questions about your retail data and get instant business insights.</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# QUICK INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">Quick Insights</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "↗  Highest Revenue",
        use_container_width=True
    ):
        st.session_state.pending_question = (
            "Which country generated the highest revenue?"
        )

with col2:
    if st.button(
        "♙  Top Customer",
        use_container_width=True
    ):
        st.session_state.pending_question = (
            "Who is the top customer by revenue?"
        )


col3, col4 = st.columns(2)

with col3:
    if st.button(
        "◇  Best Product",
        use_container_width=True
    ):
        st.session_state.pending_question = (
            "Which product generated the highest revenue?"
        )

with col4:
    if st.button(
        "◷  Best Month",
        use_container_width=True
    ):
        st.session_state.pending_question = (
            "Which month generated the highest revenue?"
        )


# =========================================================
# CHAT HISTORY
# =========================================================

if st.session_state.messages:

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"],
            avatar="👤" if message["role"] == "user" else "🤖"
        ):
            st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask a business question..."
)


# =========================================================
# QUICK QUESTION HANDLER
# =========================================================

if "pending_question" in st.session_state:

    question = st.session_state.pending_question

    del st.session_state.pending_question


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # ---------------------------------------------
    # Save user message
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(question)


    # ---------------------------------------------
    # Generate AI answer
    # ---------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Analyzing your business data..."):

            result = ask_chatbot(question)


        if result["success"]:

            answer = result["answer"]

            st.markdown(
                '<div class="assistant-label">◈ AI Insight</div>',
                unsafe_allow_html=True
            )

            # Markdown is intentionally rendered normally
            # so **bold**, lists, etc. work correctly.
            st.markdown(answer)


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


# =========================================================
# CLEAR CHAT
# =========================================================

if st.session_state.messages:

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="clear-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )