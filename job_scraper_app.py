import streamlit as st
from docx import Document
from transformers import pipeline

# Function to tailor the resume based on job description
def tailor_resume(resume_text, job_description):
    # Initialize a summarization pipeline
    summarizer = pipeline("summarization")
    
    # Break the resume into chunks of 1000 characters or less
    chunk_size = 1000
    chunks = [resume_text[i:i+chunk_size] for i in range(0, len(resume_text), chunk_size)]
    
    tailored_resume = []
    
    for chunk in chunks:
        # Summarize each chunk
        summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        tailored_resume.append(summary[0]['summary_text'])
    
    # Combine all the summarized chunks
    return " ".join(tailored_resume)

# Streamlit UI for uploading resume and providing job description
def app():
    st.title("Resume Tailoring Assistant")
    
    # Option to upload your resume
    uploaded_resume = st.file_uploader("Upload your Resume (DOCX)", type=["docx"])
    
    if uploaded_resume is not None:
        doc = Document(uploaded_resume)
        resume_text = "\n".join([para.text for para in doc.paragraphs])
    else:
        resume_text = ""

    # Input field for the job description
    job_description = st.text_area("Enter Job Description", height=300, key="job_description_area")
    
    # When user clicks the 'Tailor Resume' button
    if st.button("Tailor Resume"):
        if resume_text and job_description:
            # Tailor the resume based on the provided job description
            tailored_resume = tailor_resume(resume_text, job_description)
            
            # Display the tailored resume
            st.subheader("Tailored Resume:")
            st.write(tailored_resume)
            
            # Save the tailored resume as a new DOCX file
            tailored_doc = Document()
            tailored_doc.add_paragraph(tailored_resume)
            tailored_doc.save("/tmp/tailored_resume.docx")
            
            # Provide download link for the tailored resume
            with open("/tmp/tailored_resume.docx", "rb") as f:
                st.download_button("Download Tailored Resume", f, file_name="tailored_resume.docx")
        else:
            st.error("Please upload your resume and enter a job description to tailor your resume.")

# Run the app
if __name__ == "__main__":
    app()
