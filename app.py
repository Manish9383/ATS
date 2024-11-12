import streamlit as st
import random
import time
import google.generativeai as genai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF import to process PDFs

# Configure Gemini API with the API key from Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize model
model = genai.GenerativeModel('gemini-pro')

# Function to retrieve Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    try:
        response = model.generate_content([input_text, pdf_content, prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# PDF Processing Function
def input_pdf_setup(uploaded_file):
    if uploaded_file:
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_text_content = " ".join(page.get_text() for page in document)
        return pdf_text_content
    raise FileNotFoundError("No file uploaded")

# Function to create a PDF from text
def create_pdf(response_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, "JobFit Analyzer Response")
    text = c.beginText(50, 730)
    text.setFont("Helvetica", 10)
    text.setLeading(14)
    text.textLines(response_text)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# List of tech quotes
tech_quotes = [
    "“Technology is best when it brings people together.” – Matt Mullenweg",
    "“It has become appallingly obvious that our technology has exceeded our humanity.” – Albert Einstein",
    "“The science of today is the technology of tomorrow.” – Edward Teller",
    "“Any sufficiently advanced technology is indistinguishable from magic.” – Arthur C. Clarke",
    "“The real problem is not whether machines think but whether men do.” – B.F. Skinner"
]

# Streamlit App Configuration
st.set_page_config(page_title="Resume Analyzer", layout="centered")

# Apply custom CSS for styling and loader animation
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title-container {
        text-align: center;
        color: #264653;
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;
    }
    .subheader {
        color: #2a9d8f;
        font-size: 20px;
        text-align: center;
    }
    .button-container button {
        width: 100%;
        background-color: #2a9d8f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
        cursor: pointer;
    }
    .button-container button:hover {
        background-color: #e76f51;
        transform: scale(1.05);
    }
    .card {
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 15px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .download-button {
        background-color: #2a9d8f;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }
    .pulse-loader {
        display: inline-block;
        width: 20px;
        height: 20px;
        background-color: #2a9d8f;
        border-radius: 50%;
        animation: pulse 1s infinite ease-in-out;
        margin: 10px;
    }
    @keyframes pulse {
        0%, 100% {
            transform: scale(0.7);
        }
        50% {
            transform: scale(1.3);
        }
    }
    .quote {
        color: #264653;
        font-size: 16px;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<div class='title-container'>Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Leverage GEMINI AI to analyze and optimize your resume</div>", unsafe_allow_html=True)

# Input fields
with st.container():
    input_text = st.text_input("Enter Job Description:", key="input", help="Paste the job description here.")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])
    if uploaded_file:
        st.write("✅ PDF Uploaded Successfully")

# Prompts for various analyses
prompts = {
    "resume_review": "Review the resume against the job description, highlighting strengths and weaknesses.",
    "skill_improvement": "Suggest skills to improve for better role fit.",
    "keyword_check": "Provide missing keywords vital for the job role.",
    "percentage_match": "Calculate match percentage and final evaluation."
}

# Action Buttons and Response Handling
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
response_text = ""

if st.button("Tell Me About the Resume") and uploaded_file:
    with st.spinner(f"Loading... {random.choice(tech_quotes)}"):
        pdf_content = input_pdf_setup(uploaded_file)
        response_text = get_gemini_response(input_text, pdf_content, prompts["resume_review"])
        st.markdown(f"<div class='card'><strong>Response:</strong> {response_text}</div>", unsafe_allow_html=True)

if st.button("How Can I Improve My Skills") and uploaded_file:
    with st.spinner(f"Loading... {random.choice(tech_quotes)}"):
        pdf_content = input_pdf_setup(uploaded_file)
        response_text = get_gemini_response(input_text, pdf_content, prompts["skill_improvement"])
        st.markdown(f"<div class='card'><strong>Response:</strong> {response_text}</div>", unsafe_allow_html=True)

if st.button("What Keywords Are Missing") and uploaded_file:
    with st.spinner(f"Loading... {random.choice(tech_quotes)}"):
        pdf_content = input_pdf_setup(uploaded_file)
        response_text = get_gemini_response(input_text, pdf_content, prompts["keyword_check"])
        st.markdown(f"<div class='card'><strong>Response:</strong> {response_text}</div>", unsafe_allow_html=True)

if st.button("Calculate Percentage Match") and uploaded_file:
    with st.spinner(f"Loading... {random.choice(tech_quotes)}"):
        pdf_content = input_pdf_setup(uploaded_file)
        response_text = get_gemini_response(input_text, pdf_content, prompts["percentage_match"])
        st.markdown(f"<div class='card'><strong>Response:</strong> {response_text}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Feel Free to Ask Section
input_query = st.text_input("Feel Free to Ask Here", key="free_query", help="Enter your additional queries about the resume.")
if st.button("Answer My Query") and input_query and uploaded_file:
    with st.spinner(f"Loading... {random.choice(tech_quotes)}"):
        pdf_content = input_pdf_setup(uploaded_file)
        response_text = get_gemini_response(input_query, pdf_content, input_query)
        st.markdown(f"<div class='card'><strong>Response:</strong> {response_text}</div>", unsafe_allow_html=True)

# PDF Download Button
if response_text:
    pdf_buffer = create_pdf(response_text)
    st.download_button(
        label="📥 Download Response as PDF",
        data=pdf_buffer,
        file_name="response.pdf",
        mime="application/pdf",
        key="download-pdf"
    )
