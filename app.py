import streamlit as st
from summarize import extract_text_from_url, summarize

st.title("Laconic")
st.write("Paste an article URL and get a concise summary.")

url = st.text_input("Article URL")

if st.button("Summarize"):
    with st.spinner("Fetching and summarizing..."):
        article_text = extract_text_from_url(url)
        result = summarize(article_text)
    st.write(result)