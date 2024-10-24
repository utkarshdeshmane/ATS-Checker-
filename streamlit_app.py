import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv() 

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt_template = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.
Resume: {resume}
Description: {jd}

I want the response in one single string having the structure
{{
"JD Match":"%", 
"MissingKeywords":[], 
"Profile Summary":""
}}
"""

# CSS to add background image
page_bg_img = '''
<style>
.stApp {
    background-image: url("ats-resume-checker-1705678136705-compressed.jpeg");
    background-position: center;
    background-size: cover;
}
</style>
'''

# Inject CSS with background image
st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app content
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        # Format the input prompt with the resume and JD
        input_prompt = input_prompt_template.format(resume=resume_text, jd=jd)
        
        # Call the API to get the response
        response = get_gemini_response(input_prompt)
        
        st.subheader("ATS Evaluation Result")
        st.text(response)
