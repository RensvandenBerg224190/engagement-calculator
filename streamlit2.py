import streamlit as st
import requests
import os
from dotenv import load_dotenv

# .env bestand laden
load_dotenv()
API_KEY = os.getenv("API_KEY")

# TikTok Scraper API-instellingen
API_URL = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "tiktok-scraper2.p.rapidapi.com"
}

# Functie om video-ID uit TikTok-URL te halen
def extract_video_id(url):
    """Haalt de video-ID uit een TikTok-URL."""
    if "video/" in url:
        return url.split("video/")[1].split("?")[0]  # Pak ID na 'video/' en verwijder extra parameters
    return None

# Functie om data van TikTok-video te scrapen
def fetch_tiktok_data(video_url):
    """Haalt statistieken op van een TikTok-video via RapidAPI."""
    video_id = extract_video_id(video_url)  # Video-ID ophalen
    
    # Debugging: Print de geëxtraheerde waarden in Streamlit
    st.write(f"🔍 Input URL: {video_url}")
    st.write(f"🆔 Extracted video ID: {video_id}")
    st.write(f"🔑 API Key Loaded: {API_KEY is not None}")

    if not video_id:
        return {"URL": video_url, "Error": "Ongeldige URL"}

    params = {"video_url": video_url}  # API verwacht de volledige URL
    response = requests.get(API_URL, headers=HEADERS, params=params)

    # Debugging: Toon de ruwe API-response en statuscode
    st.write(f"📩 API Status Code: {response.status_code}")
    st.write(f"📩 API Raw Response: {response.text}")

    try:
        data = response.json()  # Probeer JSON te laden
    except ValueError:
        return {"URL": video_url, "Error": "Ongeldige JSON-response", "Raw Response": response.text}

    if "stats" in data:
        stats = data["stats"]  # Stats-object ophalen
        
        likes = stats.get("diggCount", 0)
        views = stats.get("playCount", 0)
        comments = stats.get("commentCount", 0)
        shares = stats.get("shareCount", 0)
        
        # Engagement Rate (%) = ((Likes + Comments + Shares) / Views) * 100
        engagement_rate = (
            ((likes + comments + shares) / views) * 100 if views > 0 else 0
        )

        return {
            "URL": video_url,
            "Likes": likes,
            "Views": views,
            "Comments": comments,
            "Shares": shares,
            "Engagement Rate (%)": round(engagement_rate, 2)
        }
    else:
        return {"URL": video_url, "Error": "Geen data ontvangen", "API Response": data}



# Streamlit-app UI
st.title("📊 TikTok Video Scraper")
st.write("Plak tot **50** TikTok-links hieronder en bekijk hun statistieken!")

# Tekstvak voor meerdere TikTok-links (één per regel)
input_links = st.text_area("📌 Voer TikTok-video links in (één per regel)", height=200)

# Verwerk de input als de gebruiker op de knop drukt
if st.button("🔍 Analyseer Video's"):
    video_urls = input_links.strip().split("\n")  # Splitsen op nieuwe regel
    video_urls = [url.strip() for url in video_urls if url.strip()]  # Lege regels verwijderen
    video_urls = video_urls[:50]  # Maximaal 50 video's

    if not video_urls:
        st.warning("⚠️ Voer minstens één geldige TikTok-link in!")
    else:
        st.info(f"📊 Bezig met het scrapen van {len(video_urls)} video's...")

        results = [fetch_tiktok_data(url) for url in video_urls]

        # Resultaten tonen in een tabel
        st.write("### 📈 Resultaten")
        st.table(results)
