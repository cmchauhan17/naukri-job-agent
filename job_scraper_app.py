import streamlit as st
from docx import Document

# Function to read .docx file and extract text
def read_docx(file):
    doc = Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

# Streamlit UI
st.title("AI Resume Tailoring")

# Upload Resume
uploaded_resume = st.file_uploader("Upload your Resume (.docx)", type="docx")
job_description = st.text_area("Enter Job Description")

if uploaded_resume and job_description:
    resume_text = read_docx(uploaded_resume)
    st.text_area("Your Resume Text", value=resume_text, height=300)
    
    if st.button("Tailor Resume"):
        # Here you will add the AI logic to tailor the resume
        st.write("Tailoring your resume based on the job description...")
        tailored_resume = tailor_resume(resume_text, job_description)
        
        # Save tailored resume to .docx
        tailored_resume_path = "tailored_resume.docx"
        tailored_resume.save(tailored_resume_path)
        
        st.download_button("Download Tailored Resume", tailored_resume_path)





from docx import Document

# Function to tailor the resume based on job description
def tailor_resume(resume_text, job_description):
    # Example: We will modify the "Skills" section to match the job description
    tailored_doc = Document()
    
    # Split resume text into paragraphs (this is very basic, you can enhance it)
    resume_paragraphs = resume_text.split('\n')
    
    # Modify the Skills section based on the job description
    skills_to_add = extract_skills_from_job_desc(job_description)
    
    tailored_doc.add_paragraph("Resume Tailored for Job Description")
    
    for para in resume_paragraphs:
        if "Skills" in para:  # Look for "Skills" section in the resume
            tailored_doc.add_paragraph("Skills: " + ", ".join(skills_to_add))
        else:
            tailored_doc.add_paragraph(para)
    
    return tailored_doc

# Function to extract skills from the job description
def extract_skills_from_job_desc(job_description):
    # Example of skill extraction (you can replace this with NLP techniques)
    skills = []
    keywords = ["Python", "Java", "SQL", "Leadership", "Teamwork", "Project Management"]
    
    for keyword in keywords:
        if keyword.lower() in job_description.lower():
            skills.append(keyword)
    
    return skills
