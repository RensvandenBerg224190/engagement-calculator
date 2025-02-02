import requests
import pandas as pd
import streamlit as st

# Geheimen ophalen
USERNAME = st.secrets["auth"]["username"]
PASSWORD = st.secrets["auth"]["password"]

# Loginstatus en pagina bijhouden
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# Loginpagina weergeven als gebruiker niet is ingelogd
if st.session_state.page == "login":
    st.title("Login")
    input_username = st.text_input("Gebruikersnaam")
    input_password = st.text_input("Wachtwoord", type="password")

    if st.button("Inloggen"):
        if input_username == USERNAME and input_password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "main"  # Switch naar hoofdscherm
            st.rerun()  # 🔥 Gebruik de nieuwe functie in plaats van experimental_rerun
        else:
            st.error("Onjuiste gebruikersnaam of wachtwoord!")
    st.stop()

# === Vanaf hier alleen als de gebruiker is ingelogd ===
st.title('TikTok Video Statistics')

# Functie om gegevens van een TikTok-video op te halen
def get_video_data(video_url, video_id):
    url = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
    querystring = {"video_url": video_url, "video_id": video_id}

    headers = {
        "x-rapidapi-key": st.secrets["auth"]["api_key"],  # API-key uit secrets
        "x-rapidapi-host": "tiktok-scraper2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if 'itemInfo' in data and 'itemStruct' in data['itemInfo']:
        item = data['itemInfo']['itemStruct']
        username = item.get('author', {}).get('uniqueId', 'Onbekend')
        cover_url = item.get("video", {}).get("cover", "")
        stats = item.get('stats', {})

        likes = stats.get("diggCount", 0)
        views = stats.get("playCount", 0)
        comments = stats.get("commentCount", 0)
        shares = stats.get("shareCount", 0)

        engagement_rate = ((likes + comments + shares) / views) * 100 if views > 0 else 0

        return {
            "Username": username,
            "Views": views,
            "Likes": likes,
            "Comments": comments,
            "Shares": shares,
            "Engagement Rate": engagement_rate,
            "Cover URL": cover_url
        }
    else:
        return None

# Gebruiker kan meerdere TikTok URL's invoeren
urls_input = st.text_area("Voer de TikTok video-URL's in, gescheiden door een nieuwe regel:", height=300)

if st.button("Verwerk URL's"):
    if urls_input:
        video_urls = urls_input.splitlines()
        video_data = [get_video_data(url, url.split("/")[-1]) for url in video_urls if get_video_data(url, url.split("/")[-1])]

        if video_data:
            df = pd.DataFrame(video_data)
            df['Engagement Rate'] = pd.to_numeric(df['Engagement Rate'], errors='coerce')
            df['Engagement Rate'].fillna(0, inplace=True)

            # Weergeef de engagement rate als percentage
            df['Engagement Rate (%)'] = df['Engagement Rate'].apply(lambda x: f"{round(x, 2)}%")

            # Hier behouden we de 'Engagement Rate' kolom voor de berekeningen
            df_for_calculation = df.drop(columns=["Cover URL", "Engagement Rate (%)"])

            st.write("### Video Details")
            st.dataframe(df)

            # Bereken totalen
            st.write("### Total Statistics")
            st.dataframe(pd.DataFrame([df_for_calculation.sum(numeric_only=True)]))

            # Bereken gemiddelde statistieken
            st.write("### Average Statistics")
            st.dataframe(pd.DataFrame([df_for_calculation.mean(numeric_only=True).round(2)]))
        else:
            st.error("Geen geldige gegevens gevonden voor de ingevoerde video's.")
