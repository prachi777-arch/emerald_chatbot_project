import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="Emerald AI",
    page_icon="💬",
    layout="centered"
)

# -------------------- API CONFIGURATION --------------------

api_key = os.getenv("OPENROUTER_API_KEY", "")

try:
    api_key = st.secrets.get("OPENROUTER_API_KEY", api_key)
except Exception:
    pass
model_name = "openrouter/free"
temperature = 0.7

# -------------------- EMERALD THEME --------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #071F18,
        #0B2D22,
        #103D2E
    );
    color: #F4FFF9;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p {
    color: #F4FFF9;
}

.stChatMessage {
    background: rgba(12, 57, 41, 0.78);
    border: 1px solid rgba(0, 168, 107, 0.35);
    border-radius: 16px;
}

.stButton button {
    background: #00A86B;
    color: white;
    border: 0;
    border-radius: 10px;
}

.stButton button:hover {
    background: #008F5B;
    color: white;
}

[data-testid="stChatInput"] {
    border-color: #00A86B;
}

.subtitle {
    color: #B7E8D1;
}

</style>
""", unsafe_allow_html=True)

# -------------------- CHATBOT HEADER --------------------

st.title("💬 Emerald AI")

st.markdown(
    '<p class="subtitle">A simple AI chatbot powered by LangChain.</p>',
    unsafe_allow_html=True
)

# -------------------- CHAT MEMORY --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- CHAT INPUT --------------------

prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("API key is not configured. Please contact the app administrator.")

    else:
        try:

            chat_model = ChatOpenRouter(
                model=model_name,
                api_key=api_key,
                temperature=temperature
            )

            langchain_messages = [
                SystemMessage(
                    content=(
                        "You are Emerald AI, a helpful, clear, and friendly "
                        "general-purpose assistant. Explain things simply."
                    )
                )
            ]

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

            st.error(
                "I couldn't get a response. "
                "Please check the API configuration and model availability."
            )

            with st.expander("Technical details"):
                st.code(str(error))