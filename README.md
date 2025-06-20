# 🚀 AI Web Navigator (Local LLM)

This version runs **fully offline** using `llama3` via Ollama and automates product navigation on [Bunnings](https://www.bunnings.com.au) using Playwright.

## 📦 Requirements

- [Ollama](https://ollama.com) (to run llama3 model)
  ```bash
  apt-get update && sudo apt-get install -y curl gpg
  curl -fsSL https://ollama.com/install.sh | sh
  ollama serve
  ollama pull llama3
  ```

## 🧠 Stack

- Python 3.10
- Streamlit (for UI)
- Playwright (browser automation)
- LangChain + `langchain_community.llms.Ollama`

## 🚀 Run Locally

ollama serve
In new terminal
- streamlit run main.py
### Build Image
```bash
docker build --network=host -t bunnings-navigator-local .
```

### Run App
```bash
docker run -p 8501:8501 bunnings-navigator-local
```

Make sure Ollama is running on the host.

## ✅ Features

- Entity prediction for User query, which helps in facet search. And query rephrasing
- Accepts dynamic product name
- LangChain agent (ZERO_SHOT_REACT_DESCRIPTION)
- Local reasoning via llama3
- Trajectory recovery if navigation fails
