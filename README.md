# Multi-Model Chatbot Project

A collection of [Streamlit](https://streamlit.io/) based chatbot applications utilizing different LLM providers including Google Gemini, Groq, and Mistral AI.

## 🚀 Features

- **Gemini Chatbot**: Powered by `google-genai`.
- **Groq Chatbot**: High-speed inference using Groq's API.
- **Mistral Chatbot**: Integration with Mistral AI models.
- **Session History**: Persists chat history across sessions.
- **Customizable UI**: Styled for a clean and modern user experience.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd chatbots
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install streamlit google-genai groq mistralai python-dotenv
   ```

## ⚙️ Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   MISTRAL_API_KEY=your_mistral_key
   ```

## 🏃 Usage

You can run each chatbot individually using Streamlit:

### Run Gemini Chatbot
```bash
streamlit run chatbot_gemini.py
```

### Run Groq Chatbot
```bash
streamlit run chatbot_groq.py
```

### Run Mistral Chatbot
```bash
streamlit run chatbot_mistral.py
```

## 📂 Project Structure

- `chatbot_gemini.py`: Streamlit app for Gemini AI.
- `chatbot_groq.py`: Streamlit app for Groq AI.
- `chatbot_mistral.py`: Streamlit app for Mistral AI.
- `chat_history.json`: Stores local chat logs.
- `.env`: (Ignored) Your private API keys.
- `.gitignore`: Specifies files to be ignored by Git.

## 📝 License
[MIT](LICENSE) (or specify your license)
