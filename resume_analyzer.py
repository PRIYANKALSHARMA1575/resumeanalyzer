import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure the Gemini API with your key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])  # Replace with your actual API key
model = genai.GenerativeModel('gemini-2.5-pro')  # Use the latest model

# Streamlit UI Configuration
st.set_page_config(page_title="RESUME Analyzer", page_icon="📄")
st.title("📄 RESUME Analyzer and Scorer")
st.write("Upload the RESUME and I will analyze the content based on your query.")

# PDF Upload
uploaded_file = st.file_uploader("Upload the PDF", type=["pdf"])

def extract_pdf_text(file):
    """Extract text from the uploaded PDF."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Display extracted text (for reference)
if uploaded_file is not None:
    pdf_text = extract_pdf_text(uploaded_file)
    
    st.subheader("📚 Extracted PDF Content:")
    with st.expander("Show PDF Text"):
        st.text_area("Extracted Text", pdf_text, height=200)

    # User input query
    query = st.text_area("🔎 Enter your analysis query (e.g., compare against job description, identify gaps, etc.)")

    if st.button("Analyze"):
        if pdf_text and query:
            # Create the prompt for the AI
            prompt = f"""
            You are an expert document analyzer. Analyze the following PDF content and answer the user's query. 
            
            PDF Content:
            {pdf_text}

            User Query:
            {query}

            Please provide:
            - **Matching Level:** Rate the PDF content's relevance to the query on a scale of 1-10.
            - **Areas for Improvement:** List specific areas where the content could be enhanced or refined.
            """

            try:
                response = model.generate_content(prompt)
                output = response.text

                # Display the analysis
                st.subheader("✅ Analysis Result:")
                st.markdown(output)

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:

    st.warning("Please upload a PDF file to analyze.")

