import os

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Emerald AI",
    page_icon="💬",
    layout="centered",
)

# -------------------- EMERALD GREEN THEME --------------------
st.markdown(
    """
    <style>
    :root {
        --emerald: #00A86B;
        --deep-emerald: #006B45;
        --soft-emerald: #E8F7F0;
    }
    .stApp {
        background: linear-gradient(135deg, #071F18 0%, #0B2D22 55%, #103D2E 100%);
        color: #F4FFF9;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #09271E;
        border-right: 1px solid #176B4B;
    }
    h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {
        color: #F4FFF9;
    }
    .stChatMessage {
        background: rgba(12, 57, 41, 0.78);
        border: 1px solid rgba(0, 168, 107, 0.35);
        border-radius: 16px;
    }
    .stButton button, .stDownloadButton button {
        background: #00A86B;
        color: white;
        border: 0;
        border-radius: 10px;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        background: #008F5B;
        color: white;
        border: 0;
    }
    [data-testid="stChatInput"] {
        border-color: #00A86B;
    }
    .subtitle {
        color: #B7E8D1;
        margin-top: -12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- SIDEBAR SETTINGS --------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Configure your AI model")

    api_key = st.text_input(
          "OpenRouter API key",
          type="password",
          value=os.getenv("OPENROUTER_API_KEY", ""),
          help="Your key is used only for API requests. Do not share it or upload it to GitHub.",
      )

    model_name = st.text_input(
        "Model ID",
        value="openai/gpt-oss-20b:free",
        help="Enter a model ID available in your OpenRouter account.",
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Built with Streamlit + LangChain + OpenRouter")

# -------------------- CHATBOT HEADER --------------------
st.title("💬 Emerald AI")
st.markdown(
    '<p class="subtitle">A simple AI chatbot powered by LangChain.</p>',
    unsafe_allow_html=True,
)

# -------------------- CHAT MEMORY --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- CHAT INPUT & RESPONSE --------------------
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Display and save the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        answer = "Please add your OpenRouter API key in the Settings panel on the left."
        with st.chat_message("assistant"):
            st.warning(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    elif not model_name.strip():
        answer = "Please enter a valid model ID in the Settings panel."
        with st.chat_message("assistant"):
            st.warning(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    else:
        try:
            # LangChain model connection
            chat_model = ChatOpenRouter(
                model=model_name.strip(),
                api_key=api_key,
                temperature=temperature,
            )

            # Convert Streamlit chat history into LangChain messages
            langchain_messages = [
                SystemMessage(
                    content=(
                        "You are Emerald AI, a helpful, clear, and friendly "
                        "general-purpose assistant. Explain things simply."
                    )
                )
            ]

            # Include recent conversation for context
            for item in st.session_state.messages[-16:]:
                if item["role"] == "user":
                    langchain_messages.append(
                        HumanMessage(content=item["content"])
                    )
                else:
                    langchain_messages.append(
                        AIMessage(content=item["content"])
                    )

            with st.chat_message("assistant"):
                with st.spinner("Emerald AI is thinking..."):
                    response = chat_model.invoke(langchain_messages)
                    answer = response.content

                if isinstance(answer, list):
                    answer = "\n".join(
                        part.get("text", str(part))
                        if isinstance(part, dict)
                        else str(part)
                        for part in answer
                    )

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            # Keep technical details visible during local development.
            error_message = str(error)
            st.error(
                "I couldn't get a response from the model. "
                "Check your API key, model ID, internet connection, "
                "and OpenRouter credits/limits."
            )
            with st.expander("Technical details"):
                st.code(error_message)
