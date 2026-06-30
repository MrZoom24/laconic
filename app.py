import streamlit as st
from summarize import extract_text_from_url, extract_text_from_pdf, summarize

st.title("Laconic")
st.write("Paste an article URL or upload a PDF and get a concise summary.")

input_method = st.radio("Choose input method", ["URL", "PDF"])

article_text = None

if input_method == "URL":
    url = st.text_input("Article URL")
    if st.button("Summarize") and url:
        with st.spinner("Fetching and summarizing..."):
            article_text = extract_text_from_url(url)
            result = summarize(article_text)
        st.write(result)
else:
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if st.button("Summarize") and uploaded_file:
        with st.spinner("Reading and summarizing..."):
            article_text = extract_text_from_pdf(uploaded_file)
            result = summarize(article_text)
        st.write(result)