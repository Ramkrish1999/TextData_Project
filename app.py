import streamlit as st
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests
from streamlit_lottie import st_lottie

# 📥 Download required NLTK datas
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# 🧹 Text Preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# 🔄 Load Lottie Animation from URL
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ✅ Valid working Lottie URLs
positive_lottie = load_lottie_url("https://lottie.host/799e5f0f-d83d-4447-aede-5589b38ee354/iDlsvjshcF.json")
negative_lottie = load_lottie_url("https://lottie.host/99365e68-e7f4-4644-9e1e-e84a2e02f593/7HOd38zPBR.json")
neutral_lottie = load_lottie_url("https://lottie.host/0d2c94a5-331a-4a1d-bfa0-7b2d4760042d/k7ntUrI1Zu.json")

# 🌐 Streamlit App UI
st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬", layout="centered")

st.title("💬 YouTube Comment Sentiment Analyzer")
st.markdown("Analyze sentiment of your comment with animations! 🎉")

user_input = st.text_area("📝 Enter a YouTube comment:")

if st.button("🚀 Analyze"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a comment first.")
    else:
        clean_text = preprocess_text(user_input)
        sentiment = get_sentiment(clean_text)

        st.markdown("### 💡 Sentiment Result:")
        
        if sentiment == "positive":
            st.success("😊 **Positive** — This comment has a happy vibe!")
            if positive_lottie:
                st_lottie(positive_lottie, height=250, key="pos")

        elif sentiment == "negative":
            st.error("☹️ **Negative** — This comment sounds unhappy.")
            if negative_lottie:
                st_lottie(negative_lottie, height=250, key="neg")

        else:
            st.info("😐 **Neutral** — This comment feels balanced.")
            if neutral_lottie:
                st_lottie(neutral_lottie, height=250, key="neu")

# Footer
st.markdown("---")
st.caption("🧠 Built with Streamlit + TextBlob + Lottie • Inspired by HuggingFace Spaces")
