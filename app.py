import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Card styling */
    .result-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Score display */
    .score-display {
        font-size: 64px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d9ff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Input labels */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background: rgba(0,255,136,0.1);
        border: 1px solid rgba(0,255,136,0.3);
        border-radius: 12px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)


def set_api_key(api_key: str, provider: str):
    """Set the API key as environment variable."""
    if provider == "Google AI":
        os.environ["GOOGLE_API_KEY"] = api_key
    else:
        os.environ["OPENAI_API_KEY"] = api_key


def run_analysis(resume_text: str, job_url: str):
    """Run the crew analysis and return results."""
    import tempfile
    from resume_analyzer.crew import ResumeAnalyzerCrew
    
    # Save resume text to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(resume_text)
        temp_resume_path = f.name
    
    try:
        crew_instance = ResumeAnalyzerCrew()
        inputs = {
            'resume_path': temp_resume_path,
            'job_url': job_url
        }
        result = crew_instance.crew().kickoff(inputs=inputs)
        return str(result)
    finally:
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)



def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    import pypdf
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def main():
    # Sidebar - Configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")
        
        provider = st.selectbox(
            "LLM Provider",
            ["Google AI", "OpenAI"],
            help="Select your LLM provider"
        )
        
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Enter your API key...",
            help="Your API key will be used to call the LLM"
        )
        
        if api_key:
            set_api_key(api_key, provider)
            st.success("✓ API Key configured")
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. Enter your API key above
        2. Upload your Resume PDF
        3. Enter the job posting URL
        4. Click **Analyze**
        """)
    
    # Main content
    st.markdown("# 📄 Resume Analyzer")
    st.markdown("*AI-powered resume analysis and job matching*")
    st.markdown("---")
    
    # Two-column layout for inputs
    col1, col2 = st.columns([2, 1])
    
    resume_text = ""
    
    with col1:
        st.markdown("### 📝 Your Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type="pdf",
            help="Upload your resume in PDF format"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Processing PDF..."):
                    resume_text = extract_text_from_pdf(uploaded_file)
                st.success("✓ Resume uploaded and processed")
                with st.expander("View extracted text"):
                    st.text(resume_text)
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
    
    with col2:
        st.markdown("### 🔗 Job Posting")
        job_url = st.text_input(
            "Job URL",
            placeholder="https://example.com/job/...",
            label_visibility="collapsed"
        )
        
        st.markdown("###")  # Spacer
        st.markdown("###")  # Spacer
        
        analyze_clicked = st.button("🚀 Analyze Match", use_container_width=True)
    
    st.markdown("---")
    
    # Run analysis
    if analyze_clicked:
        # Validation
        if not api_key:
            st.error("⚠️ Please enter your API key in the sidebar")
            return
        
        if not uploaded_file:
            st.error("⚠️ Please upload your resume PDF")
            return

        if not resume_text.strip():
            st.error("⚠️ Could not extract text from the PDF. Please try a different file.")
            return
        
        if not job_url.strip():
            st.error("⚠️ Please enter the job posting URL")
            return
        
        # Run the analysis
        with st.spinner("🔍 Analyzing your resume against the job description..."):
            try:
                result = run_analysis(resume_text, job_url)
                
                st.markdown("## 📊 Analysis Results")
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.markdown("**Troubleshooting:**")
                st.markdown("- Verify your API key is correct")
                st.markdown("- Check that the job URL is accessible")
                st.markdown("- Ensure your resume text is properly formatted")


if __name__ == "__main__":
    main()
