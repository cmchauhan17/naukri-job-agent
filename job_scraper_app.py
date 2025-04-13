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



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--headless")  # run in headless mode
    options.add_argument("--no-sandbox")  # prevent sandboxing issues
    options.add_argument("--disable-dev-shm-usage")  # prevent memory issues

    # Set the correct path using the executable_path argument
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    return driver

job_titles = []
job_links = []

if job_keyword:
    st.info("Searching Naukri.com...")
    try:
        driver = get_driver()
        search_url = f"https://www.naukri.com/{job_keyword.replace(' ', '-')}-jobs"
        driver.get(search_url)
        time.sleep(3)  # wait for page to load

        jobs = driver.find_elements(By.CLASS_NAME, "jobTuple")[:10]

        for job in jobs:
            try:
                title = job.find_element(By.CLASS_NAME, "title").text
                link = job.find_element(By.CLASS_NAME, "title").get_attribute("href")
                company = job.find_element(By.CLASS_NAME, "subTitle").text
                location = job.find_element(By.CLASS_NAME, "location").text
                job_titles.append(f"{title} | {company} | {location}")
                job_links.append(link)
            except Exception as e:
                continue

        driver.quit()

        if job_titles:
            selected_index = st.selectbox("Select a job to tailor your resume for:", range(len(job_titles)), format_func=lambda x: job_titles[x])
            selected_link = job_links[selected_index]

            st.markdown("### 📋 Job Description Preview")
            driver = get_driver()
            driver.get(selected_link)
            time.sleep(3)

            try:
                job_desc_elem = driver.find_element(By.CLASS_NAME, "dang-inner-html")
                job_desc = job_desc_elem.text
            except:
                job_desc = "Description not found."

            driver.quit()
            st.text_area("Job Description", value=job_desc, height=300)

            st.markdown("### ✍️ Choose Resume Rewrite Format")
            rewrite_style = st.radio(
                "Select a rewrite tone/style:",
                options=["Conservative", "Bold", "Keyword-Heavy", "Soft"],
                index=0
            )
            st.success(f"'{rewrite_style}' style selected. Ready to tailor your resume!")
        else:
            st.warning("No job cards found.")
    except Exception as e:
        st.error(f"Error fetching job listings: {e}")



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
