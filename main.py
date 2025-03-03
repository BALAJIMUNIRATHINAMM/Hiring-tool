import pandas as pd
import streamlit as st
import io
import time

# Page Configuration
st.set_page_config(
    page_title="Hiring Deliverable-BD sales",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header

# Add a header with a divider
st.header('Braindesk Data Project Optimization Pullouts', divider='rainbow')
st.markdown("<h1 style='text-align: center; color: #4b72b0;'>Hiring Deliverable Data Cleaner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff6347;'>Upload your CSV or Excel file to clean and analyze the hiring data</h3>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Record start time
    start_time = time.time()

    # Load the file into a DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean data
    df = df.dropna(subset=['mvp_company_name'])
    #df['business_function'] = df['buisness_function'].astype('str')
    df.replace({
        '"]': '',
        '\["': '',
        '\[]': '-',
        '","': ';'
    }, regex=True, inplace=True)
    df.fillna('-', inplace=True)
    df.drop_duplicates(inplace=True)

    # Calculate processing time
    processing_time = time.time() - start_time

    # Apply custom CSS for central alignment of hyphens
    st.markdown(
        """
        <style>
        table tbody tr td:has(span:contains("-")) {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display data information
    st.markdown("<h4 style='color: #2e8b57;'>Data Information</h4>", unsafe_allow_html=True)
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Display the DataFrame with central alignment for hyphens
    st.markdown("<h4 style='color: #2e8b57;'>Job Data Preview</h4>", unsafe_allow_html=True)
    st.dataframe(df)

    # Allow the user to download the cleaned data
    st.markdown("<h4 style='color: #2e8b57;'>Download Cleaned Data</h4>", unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv',
        use_container_width=True
    )

    # Display processing time
    st.markdown(f"<p style='text-align: center; color: #4b72b0;'>Processing time: {processing_time:.2f} seconds</p>", unsafe_allow_html=True)

else:
    st.warning("Please upload a CSV or Excel file to start processing.")

# Footer
footer = """
<style>
.footer {position: fixed; left: 0; bottom: 0; width: 100%; background-color: #4b72b0; color: white; text-align: center; padding: 10px;}
</style>
<div class="footer">
<p>&copy; 2025 All Rights Reserved.</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
