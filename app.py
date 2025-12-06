import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from transformers import pipeline
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Summ.AI | Smart Text Summarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #6C63FF;
    }
    .stButton>button {
        background: linear-gradient(45deg, #6C63FF, #00B4D8);
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL LOADING (CACHED) ---
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

@st.cache_resource
def load_transformer_model():
    return pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="pt")

# --- SUMMARIZATION FUNCTIONS ---
def extractive_summarizer(text, num_sentences):
    nlp = load_spacy_model()
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc 
              if not token.is_stop and not token.is_punct and token.text != '\n']
    word_freq = Counter(tokens)
    if not word_freq: return "Not enough data."
    max_freq = max(word_freq.values())
    for word in word_freq.keys(): word_freq[word] /= max_freq
    sent_token = [sent.text for sent in doc.sents]
    sent_score = {}
    for sent in sent_token:
        for word in sent.split():
            if word.lower() in word_freq.keys():
                sent_score[sent] = sent_score.get(sent, 0) + word_freq[word]
    return " ".join(nlargest(num_sentences, sent_score, key=sent_score.get))

def abstractive_summarizer(text):
    summarizer = load_transformer_model()
    input_len = len(text.split())
    # Dynamic parameter adjustment
    max_len = min(150, max(40, int(input_len * 0.5)))
    min_len = max(20, int(input_len * 0.2))
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    algo_type = st.selectbox("Choose Algorithm", ["Extractive (Spacy)", "Abstractive (T5-Deep Learning)"])
    
    if algo_type == "Extractive (Spacy)":
        st.info("Extractive: Selects the most important sentences from the original text.")
        sent_count = st.slider("Sentence Count", 1, 10, 3)
    else:
        st.info("Abstractive: Generates new sentences to paraphrase the text (Slower but more human-like).")

    st.markdown("---")
    st.write("Made with ❤️ by Yash")

# --- MAIN LAYOUT ---
st.markdown('<p class="big-font">✨ Summ.AI <span style="color:gray; font-size:20px">| Intelligent Text Summarization</span></p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Summarizer", "ℹ️ How it Works"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("### 📥 Input Text")
        raw_text = st.text_area("Paste your article here...", height=300, placeholder="Enter text to summarize...")
        
        # Analyze button
        if st.button("🚀 Generate Summary"):
            if not raw_text:
                st.warning("⚠️ Please enter some text to summarize.")
            else:
                with col2:
                    st.markdown("### 📤 Summary Result")
                    with st.spinner("Analyzing text and generating summary..."):
                        start_time = time.time()
                        
                        if algo_type == "Extractive (Spacy)":
                            final_summary = extractive_summarizer(raw_text, sent_count)
                        else:
                            final_summary = abstractive_summarizer(raw_text)
                        
                        end_time = time.time()
                        
                        # Display Summary
                        st.success(final_summary)
                        
                        # Metrics Section
                        st.markdown("---")
                        m1, m2, m3 = st.columns(3)
                        
                        # Calculate metrics
                        orig_len = len(raw_text.split())
                        sum_len = len(final_summary.split())
                        reduction = round(((orig_len - sum_len) / orig_len) * 100, 2)
                        
                        m1.metric("Original Words", orig_len)
                        m2.metric("Summary Words", sum_len)
                        m3.metric("Reduction", f"{reduction}%")
                        st.caption(f"Time taken: {round(end_time - start_time, 2)} seconds")

with tab2:
    st.markdown("""
    ### About the Algorithms
    
    **1. Extractive Summarization (Spacy):**
    * **How it works:** It calculates the frequency of words in the text and scores sentences based on the importance of the words they contain. The top-ranked sentences are returned.
    * **Pros:** Fast, factual (doesn't hallucinate info).
    * **Cons:** Can feel disjointed.
    
    **2. Abstractive Summarization (T5 Transformer):**
    * **How it works:** Uses a Deep Learning model (T5 - Text-to-Text Transfer Transformer) trained on massive datasets to understand context and rewrite the summary.
    * **Pros:** Fluent, human-like summaries.
    * **Cons:** Slower, computationally heavy.
    """)