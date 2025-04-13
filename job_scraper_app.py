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
