import anthropic
import streamlit as st
from summarize import extract_text_from_url, extract_text_from_pdf, summarize

st.title("Laconic")
st.write("Paste an article URL or upload a PDF and get a concise summary.")

api_key = st.text_input("Your Anthropic API key", type="password", help="Get one at console.anthropic.com")


def run_summary(extract_fn, source, api_key):
    try:
        with st.spinner("Summarizing..."):
            article_text = extract_fn(source)
            result = summarize(article_text, api_key)
        
        st.subheader("Summary")
        st.write(result["summary"])

        if result["jargon"]:
            st.subheader("Key Terms")
            for item in result["jargon"]:
                st.markdown(f"**{item['term']}** - {item['explanation']}")
    except ValueError as e:
        st.error(str(e))
    except anthropic.AuthenticationError:
        st.error("Invalid API key. Please check it and try again.")
    except anthropic.RateLimitError:
        st.error("Rate limited by the Anthropic API. Please wait a moment and try again.")
    except anthropic.APIStatusError as e:
        st.error(f"Anthropic API error: {e.message}")
    except anthropic.APIConnectionError:
        st.error("Couldn't reach the Anthropic API. Check your internet connection.")

input_method = st.radio("Choose input method", ["URL", "PDF"])

if input_method == "URL":
    url = st.text_input("Article URL")
    if st.button("Summarize") and url and api_key:
        run_summary(extract_text_from_url, url, api_key)
else:
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if st.button("Summarize") and uploaded_file and api_key:
        run_summary(extract_text_from_pdf, uploaded_file, api_key)