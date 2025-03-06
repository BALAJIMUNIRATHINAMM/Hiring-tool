import pandas as pd
import streamlit as st
import io
import time
from format_jd import DashboardFormatter

# Ensure that the DashboardFormatter class is correctly defined in the format_jd module

# Page Configuration
st.set_page_config(
    page_title="Hiring Deliverable",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Increase the max elements allowed for Pandas Styler
pd.set_option("styler.render.max_elements", 500000)

# Header
st.markdown("<h1 style='text-align: center; color: #4b72b0;'>Hiring Deliverable Data Cleaner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff6347;'>Upload your CSV or Excel file to clean and analyze the hiring data</h3>", unsafe_allow_html=True)

# File uploader for data file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Record start time
    start_time = time.time()

    # Load the file into a DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Data Cleaning
    if 'mvp_company_name' in df.columns:
        df = df.dropna(subset=['mvp_company_name'])
    
    if 'business_function' in df.columns:
        df['business_function'] = df['business_function'].astype(str)
    
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

    # Display data information
    st.markdown("<h4 style='color: #2e8b57;'>Data Information</h4>", unsafe_allow_html=True)
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Display the DataFrame (limited to first 500 rows to avoid rendering issues)
    st.markdown("<h4 style='color: #2e8b57;'>Job Data Preview</h4>", unsafe_allow_html=True)
    st.dataframe(df.head(500))

    # Allow the user to download the cleaned data
    st.markdown("<h4 style='color: #2e8b57;'>Download Cleaned Data</h4>", unsafe_allow_html=True)
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv',
        use_container_width=True
    )

    # Custom title input
    custom_title = st.text_input("Enter Custom Title for Formatted File", "Requested Accounts")
    
    # Formatter file upload
    formatter_file = st.file_uploader("Upload Formatter File (if required)", type=["xlsx"])
    if formatter_file is not None:
        # Convert the uploaded formatter file to a BytesIO object for DashboardFormatter
        formatter_file_bytes = io.BytesIO(formatter_file.getvalue())
        formatter = DashboardFormatter(formatter_file_bytes)
        output_name = "formatter_jd.xlsx"
        # Perform formatting (assuming the method modifies the workbook internally)
        formatter.formatter_jd(df)
        formatter.save(output_name)
        
        st.download_button(
            label='Download Formatted File',
            data=open(output_name, 'rb').read(),
            file_name=output_name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
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
