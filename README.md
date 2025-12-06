# 📝 AI Text Summarizer

This is a simple and powerful **AI-based text summarization web app** built with **Streamlit**. It supports two modes:

- **Extractive Summarization** using SpaCy and word frequency.
- **Abstractive Summarization** using HuggingFace Transformers (BART-based model).

---

## 🚀 Features

- ✍️ Paste any long text or article.
- 🔧 Choose between **Extractive** or **Abstractive** summarization modes.
- 💬 Summarize using either rules or deep learning.
- 🎨 Clean and colorful user interface with custom styling.

---

## 🧠 How It Works

### 🔹 Extractive Summarization:
Uses **SpaCy** to identify the most important sentences based on word frequency (ignoring stopwords and punctuation).

### 🔹 Abstractive Summarization:
Uses **HuggingFace's BART transformer** model to generate a new summary with rephrased content.

---

## 🧰 Tech Stack

- Python 3
- Streamlit
- SpaCy
- Transformers (HuggingFace)
- PyTorch

---

## 🔧 Installation (Local Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/Yash-Coder-07/TextSummarization.git
cd TextSummarization
