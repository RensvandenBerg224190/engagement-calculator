import streamlit as st
import requests
import os
from dotenv import load_dotenv

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
