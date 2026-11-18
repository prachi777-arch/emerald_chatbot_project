# 💚 Emerald AI — AI Chatbot

Emerald AI is a web-based AI chatbot built using Python, Streamlit, LangChain and OpenRouter. It provides an interactive conversational experience through a simple and user-friendly interface.

## 🌟 Features

- AI-powered conversational responses.
- Interactive chat interface.
- Conversation history during the session.
- Customizable creativity (temperature).
- Integration with OpenRouter.
- Free model routing through OpenRouter.
- Secure API key input.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| LangChain | AI application framework |
| OpenRouter | AI model API |
| Git & GitHub | Version control and code hosting |

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd emerald_chatbot_project
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

## 🔑 API Configuration

Emerald AI uses an OpenRouter API key.

You can enter your API key through the application sidebar when running locally.

For deployment, configure the key securely using Streamlit Cloud Secrets:

```toml
OPENROUTER_API_KEY = "your_api_key"
```

Never commit API keys or other sensitive credentials to GitHub.

## 🌐 Live Demo

## 🌐 Live Demo
[Launch Emerald AI](https://emeraldchatbotproject-n9fcnrhyetrsfmj4gyxpsy.streamlit.app/)
## 👩‍💻 Project

**Emerald AI** is a beginner-friendly AI development project created to explore conversational AI, API integration and web application deployment.

---

*Built with Python and curiosity. 💚*