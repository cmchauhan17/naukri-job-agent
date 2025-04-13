import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🔎 Naukri Job Finder")

job_keyword = st.text_input("Enter job title or keyword (e.g., Data Analyst, Procurement Manager)")

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

        st.subheader(f"Top {len(job_cards)} Jobs for '{job_keyword}':")
        for i, card in enumerate(job_cards):
            title = card.find('a', class_='title').text.strip()
            company = card.find('a', class_='subTitle').text.strip()
            location = card.find('li', class_='location').text.strip()
            link = card.find('a', class_='title')['href']

            st.markdown(f"**{i+1}. [{title}]({link})**  \n*Company:* {company}  \n*Location:* {location}", unsafe_allow_html=True)
    else:
        st.error("Failed to fetch job data. Try again later.")

job_titles = []
job_links = []

for i, card in enumerate(job_cards):
    title = card.find('a', class_='title').text.strip()
    company = card.find('a', class_='subTitle').text.strip()
    location = card.find('li', class_='location').text.strip()
    link = card.find('a', class_='title')['href']

    full_title = f"{title} | {company} | {location}"
    job_titles.append(full_title)
    job_links.append(link)

# Let user pick a job from the list
selected_index = st.selectbox("Select a job to tailor your resume for:", range(len(job_titles)), format_func=lambda x: job_titles[x])
selected_link = job_links[selected_index]


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
