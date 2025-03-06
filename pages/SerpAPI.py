import streamlit as st
import requests
import pandas as pd
import time
import chardet

# SerpAPI Configuration
SERP_API_KEY = "your_serpapi_key"  # Replace with your SerpAPI Key
GOOGLE_SEARCH_URL = "https://serpapi.com/search"

def detect_encoding(file):
    """Detects file encoding to handle UnicodeDecodeError"""
    raw_data = file.read()
    file.seek(0)  # Reset file pointer
    result = chardet.detect(raw_data)
    return result["encoding"]

def load_csv(uploaded_file):
    """Loads a CSV file with proper encoding detection"""
    encoding = detect_encoding(uploaded_file)
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
        return df
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
        return None

def get_openreview_urls(speakers, topics):
    """Extracts OpenReview URLs from Google Search results"""
    query_list = [f"{speaker} {topic} site:openreview.net" for speaker in speakers for topic in topics]
    openreview_urls = set()

    for query in query_list:
        try:
            params = {"q": query, "api_key": SERP_API_KEY, "num": 10}
            response = requests.get(GOOGLE_SEARCH_URL, params=params)
            data = response.json()

            if "organic_results" in data:
                for result in data["organic_results"]:
                    url = result.get("link", "")
                    if "openreview.net" in url:
                        openreview_urls.add(url)

            time.sleep(1)  # Prevent hitting API limits
        except Exception as e:
            st.error(f"❌ API request failed: {e}")

    return list(openreview_urls)

# Streamlit UI
st.title("🔍 OpenReview URL Extractor")

# File Upload Option
uploaded_file = st.file_uploader("📂 Upload CSV with 'Speaker' and 'Topic' columns", type=["csv"])

speakers, topics = [], []

if uploaded_file:
    df = load_csv(uploaded_file)
    if df is not None and "Speaker" in df.columns and "Topic" in df.columns:
        speakers = df["Speaker"].dropna().tolist()
        topics = df["Topic"].dropna().tolist()
        st.success("✅ CSV uploaded successfully!")
    else:
        st.error("❌ CSV must contain 'Speaker' and 'Topic' columns!")
else:
    speakers = st.text_area("Enter Speaker Names (comma-separated)").split(",")
    topics = st.text_area("Enter Topics (comma-separated)").split(",")

# Clean input lists
speakers = [s.strip() for s in speakers if s.strip()]
topics = [t.strip() for t in topics if t.strip()]

# Extract URLs Button
if st.button("🔎 Extract OpenReview URLs"):
    if not speakers or not topics:
        st.error("❌ Please enter at least one speaker and one topic!")
    else:
        st.info("⏳ Searching for OpenReview URLs... Please wait.")
        urls = get_openreview_urls(speakers, topics)

        if urls:
            df_results = pd.DataFrame({"OpenReview URLs": urls})
            st.success(f"✅ Found {len(urls)} OpenReview URLs!")
            st.dataframe(df_results)

            # Save CSV File
            csv_filename = "openreview_urls.csv"
            df_results.to_csv(csv_filename, index=False)

            # Download Button
            st.download_button(
                label="📥 Download CSV",
                data=df_results.to_csv(index=False),
                file_name=csv_filename,
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No OpenReview URLs found!")
