import streamlit as st
import requests
import os
from dotenv import load_dotenv

# .env bestand laden
load_dotenv()
API_KEY = os.getenv("API_KEY")

# TikTok Scraper API-instellingen
API_URL = "https://tiktok-scraper2.p.rapidapi.com/video"
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
    
    if not video_id:
        return {"URL": video_url, "Error": "Ongeldige URL"}

    params = {"id": video_id}
    response = requests.get(API_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            likes = data["data"].get("digg_count", 0)
            views = data["data"].get("play_count", 0)
            comments = data["data"].get("comment_count", 0)
            shares = data["data"].get("share_count", 0)
            
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
            return {"URL": video_url, "Error": "Geen data ontvangen"}
    else:
        return {"URL": video_url, "Error": f"Foutcode {response.status_code}"}

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
