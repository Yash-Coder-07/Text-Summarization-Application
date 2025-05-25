import streamlit as st
from collections import Counter
from transformers import pipeline
import spacy

# 🌐 Streamlit page config
st.set_page_config(page_title="Text Summarizer", layout="centered", page_icon="📝")

# 🎨 Custom CSS
st.markdown("""
    <style>
        textarea, input { color: black !important; }
        .stButton>button {
            background-color: #3e64ff;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stTextArea textarea {
            background-color: #f0f2f6;
        }
        .block-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #3e64ff;
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 Load models with caching
@st.cache_resource
def load_spacy_model():
    import en_core_web_sm
    return en_core_web_sm.load()

@st.cache_resource
def load_abstractive_summarizer():
    return pipeline("summarization")

# 🧠 Extractive summarization
def extractive_summary(text, nlp_model, max_sentences=3):
    doc = nlp_model(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(tokens)
    max_freq = max(word_freq.values()) if word_freq else 1
    for word in word_freq:
        word_freq[word] /= max_freq

    sent_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_freq:
                sent_scores[sent] = sent_scores.get(sent, 0) + word_freq[word.text.lower()]

    top_sentences = sorted(sent_scores, key=sent_scores.get, reverse=True)[:max_sentences]
    return ' '.join([sent.text.strip() for sent in top_sentences])

# 🖼️ UI
st.title("📝 AI Text Summarizer")

mode = st.sidebar.selectbox(
    "Choose Summarization Type",
    ("Extractive (SpaCy + Word Frequency)", "Abstractive (Transformer Model)")
)

st.subheader("✍️ Enter Your Text")
text_input = st.text_area("Paste a long paragraph or article here", height=250)

# 🔘 Button
if st.button("Generate Summary"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        if "Extractive" in mode:
            nlp = load_spacy_model()
            summary = extractive_summary(text_input, nlp)
        else:
            summarizer = load_abstractive_summarizer()
            try:
                result = summarizer(text_input, max_length=130, min_length=30, do_sample=False)
                summary = result[0]['summary_text']
            except Exception as e:
                summary = f"⚠️ Error: {e}"

        st.subheader("📌 Summary:")
        st.success(summary)
