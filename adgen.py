import streamlit as st
import openai
import requests
import json

# Load secrets
openai.api_key = st.secrets["openai"]["api_key"]
serp_api_key = st.secrets["serpapi"]["api_key"]

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

# Function to get data from SerpAPI
def get_page_content(url):
    serpapi_url = f"https://serpapi.com/search.json?api_key={serp_api_key}&url={url}"
    response = requests.get(serpapi_url)
    if response.status_code == 200:
        return response.json().get('content')
    else:
        st.error("Failed to retrieve page content")
        return None

# Function to generate ads with OpenAI
def generate_ad_content(page_content, description, business_type, channels):
    prompt = f"""
    Create online ads for the following business type: {business_type}.
    Product Description: {description if description else page_content}
    Platforms: {', '.join(channels)}.
    Provide best practices and keyword recommendations for each selected platform.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text

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
