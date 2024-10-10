import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Load secrets
api_key = st.secrets["openai"]["api_key"]

# App title and introduction
st.title("Ad Creator for Online Platforms")
st.write("Enter the URL of your business/product page and optionally a product/service description. Select the platforms and business type to create ads.")

# URL and optional product description input
url = st.text_input("Enter your business/product page URL")
description = st.text_area("Optional: Provide a short description of your product or service")

# Channel selection
channels = st.multiselect(
    "Select ad platforms to create ads for:",
    ["Google PPC", "Facebook", "LinkedIn", "Twitter"]
)

# Business type selection
business_type = st.selectbox(
    "Select the type of your business:",
    ["E-commerce", "Services (Education, Consulting, Professional Services)", "Local Business", "Technology (Software, etc.)"]
)

# Function to scrape page content using BeautifulSoup
def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            # Get visible text content of the page
            page_content = ' '.join([p.get_text() for p in soup.find_all('p')])
            return page_content
        else:
            st.error(f"Failed to retrieve page content. HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to generate ads with GPT-4o-mini
def generate_ad_content(page_content, description, business_type, channels):
    prompt = f"""
    Create online ads for the following business type: {business_type}.
    Product Description: {description if description else page_content}
    Platforms: {', '.join(channels)}.
    Provide best practices and keyword recommendations for each selected platform.
    """
    
    client = openai.Client(api_key=api_key)  # Initialize the OpenAI client with API key
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at generating online ad content for different platforms."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return completion['choices'][0]['message']['content']

# Submit button
if st.button("Generate Ads"):
    if url:
        page_content = get_page_content(url)
        if page_content:
            ad_content = generate_ad_content(page_content, description, business_type, channels)
            st.write("### Generated Ads and Keyword Recommendations:")
            st.text(ad_content)

            # Download button for ads and keyword recommendations
            st.download_button("Download Ad Content", ad_content, file_name="ad_content.txt")
    else:
        st.error("Please enter a valid URL.")
