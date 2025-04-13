import streamlit as st
import requests
from bs4 import BeautifulSoup

job_titles = []
job_links = []

if job_keyword:
    st.info("Searching Naukri.com...")

    url = f"https://www.naukri.com/{job_keyword.replace(' ', '-')}-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all('article', class_='jobTuple')[:10]

        if job_cards:
            for i, card in enumerate(job_cards):
                try:
                    title = card.find('a', class_='title').text.strip()
                    company = card.find('a', class_='subTitle').text.strip()
                    location = card.find('li', class_='location').text.strip()
                    link = card.find('a', class_='title')['href']

                    full_title = f"{title} | {company} | {location}"
                    job_titles.append(full_title)
                    job_links.append(link)
                except:
                    continue  # skip cards with missing data

            if job_titles:
                selected_index = st.selectbox("Select a job to tailor your resume for:", range(len(job_titles)), format_func=lambda x: job_titles[x])
                selected_link = job_links[selected_index]

                st.markdown("### 📋 Job Description Preview")

                job_desc = ""
                try:
                    job_resp = requests.get(selected_link, headers=headers)
                    if job_resp.status_code == 200:
                        job_soup = BeautifulSoup(job_resp.text, "html.parser")
                        jd_div = job_soup.find('div', class_='dang-inner-html')
                        job_desc = jd_div.get_text(separator="\n").strip() if jd_div else "Description not found."
                    else:
                        job_desc = "Failed to load job description."
                except Exception as e:
                    job_desc = f"Error: {str(e)}"

                st.text_area("Job Description", value=job_desc, height=300)

                st.markdown("### ✍️ Choose Resume Rewrite Format")

                rewrite_style = st.radio(
                    "Select a rewrite tone/style:",
                    options=["Conservative", "Bold", "Keyword-Heavy", "Soft"],
                    index=0
                )

                st.success(f"'{rewrite_style}' style selected. Ready to tailor your resume!")
            else:
                st.warning("No job listings found. Try a different keyword.")
        else:
            st.warning("Couldn't find job cards. Naukri might have changed layout.")
    else:
        st.error("Failed to fetch job data. Try again later.")

from docx import Document

st.markdown("---")
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Upload a .docx resume", type=["docx"])

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

if uploaded_file:
    resume_text = extract_text_from_docx(uploaded_file)
    st.success("Resume uploaded successfully!")
    
    # Optional: Show a preview of resume
    with st.expander("🔍 Click to preview your resume text"):
        st.text(resume_text)
