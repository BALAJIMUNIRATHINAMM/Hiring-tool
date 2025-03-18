import pandas as pd
import streamlit as st
import io
import time
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from format_jd import DashboardFormatter

# Ensure that the DashboardFormatter class is correctly defined in the format_jd module
=======
from ast import literal_eval
>>>>>>> Stashed changes
=======
from ast import literal_eval
>>>>>>> Stashed changes

# Page Configuration
st.set_page_config(
    page_title="Hiring Deliverable",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded"
)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Increase the max elements allowed for Pandas Styler
pd.set_option("styler.render.max_elements", 500000)

# Header
st.markdown("<h1 style='text-align: center; color: #4b72b0;'>Hiring Deliverable Data Cleaner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff6347;'>Upload your CSV or Excel file to clean and analyze the hiring data</h3>", unsafe_allow_html=True)
=======
=======
>>>>>>> Stashed changes
# Header
st.markdown("""
    <h1 style='text-align: center; color: #4b72b0;'>Hiring Deliverable Data Cleaner</h1>
    <h3 style='text-align: center; color: #ff6347;'>Upload your CSV or Excel file to clean and analyze the hiring data</h3>
""", unsafe_allow_html=True)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

# File uploader for data file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

def safe_eval(value):
    """Safely evaluate string representations of lists."""
    try:
        return literal_eval(value) if isinstance(value, str) else value
    except (ValueError, SyntaxError):
        return []

if uploaded_file is not None:
    start_time = time.time()

    # Load the file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
    
=======
=======
>>>>>>> Stashed changes
    # Ensure required column exists
    if 'mvp_company_name' not in df.columns:
        st.error("Error: The required column 'mvp_company_name' is missing from the file.")
        st.stop()

    # Data Cleaning
    df.dropna(subset=['mvp_company_name'], inplace=True)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    df.fillna('-', inplace=True)
    df.replace({
        r'\"]': '',
        r'\["': '',
        r'\[]': '-',
        r'","': ';'
    }, regex=True, inplace=True)
    
    df['business_function'] = df['business_function'].apply(lambda x: x.split(';') if isinstance(x, str) and ';' in x else x)
    df.drop_duplicates(inplace=True)
    processing_time = time.time() - start_time

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Display data information
=======
    # Display Data Information
>>>>>>> Stashed changes
=======
    # Display Data Information
>>>>>>> Stashed changes
    st.markdown("<h4 style='color: #2e8b57;'>Data Information</h4>", unsafe_allow_html=True)
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Display the DataFrame (limited to first 500 rows to avoid rendering issues)
=======
    # Display Data Preview
>>>>>>> Stashed changes
=======
    # Display Data Preview
>>>>>>> Stashed changes
    st.markdown("<h4 style='color: #2e8b57;'>Job Data Preview</h4>", unsafe_allow_html=True)
    st.dataframe(df.head(500))

    # Download Cleaned Data
    st.markdown("<h4 style='color: #2e8b57;'>Download Cleaned Data</h4>", unsafe_allow_html=True)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    csv = df.to_csv(index=False, encoding='utf-8-sig')
=======
    csv = df.to_csv(index=False).encode('utf-8')
>>>>>>> Stashed changes
=======
    csv = df.to_csv(index=False).encode('utf-8')
>>>>>>> Stashed changes
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv'
    )

<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
=======
    # Display Processing Time
>>>>>>> Stashed changes
=======
    # Display Processing Time
>>>>>>> Stashed changes
    st.markdown(f"<p style='text-align: center; color: #4b72b0;'>Processing time: {processing_time:.2f} seconds</p>", unsafe_allow_html=True)
else:
    st.warning("Please upload a CSV or Excel file to start processing.")

# Footer
st.markdown("""
    <style>
    .footer {position: fixed; left: 0; bottom: 0; width: 100%; background-color: #4b72b0; color: white; text-align: center; padding: 10px;}
    </style>
    <div class="footer">
    <p>Developed with ❤️ by Draup Suite | &copy; 2024 All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
