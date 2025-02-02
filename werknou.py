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


# Functie om gegevens van een TikTok-video op te halen
def get_video_data(video_url, video_id):
    url = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
    querystring = {"video_url": video_url, "video_id": video_id}

    headers = {
        "x-rapidapi-key": "87f7d04a69msh064fc11c54bbcd5p1e1223jsn039442082ea2",
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

# Functie om gegevens van meerdere video's op te halen
def get_multiple_videos_data(video_urls):
    video_data = []
    for video_url in video_urls:
        video_id = video_url.split("/")[-1]  
        data = get_video_data(video_url, video_id)
        if data:
            video_data.append(data)
    return video_data

# Functie om de gemiddelde statistieken te berekenen
def calculate_averages(df):
    averages = {
        "Views": round(df["Views"].mean(), 2),
        "Likes": round(df["Likes"].mean(), 2),
        "Comments": round(df["Comments"].mean(), 2),
        "Shares": round(df["Shares"].mean(), 2),
        "Engagement Rate": round(df["Engagement Rate"].mean(), 2)
    }
    return averages

# Functie om de totale sommen van de statistieken te berekenen
def calculate_totals(df):
    totals = {
        "Views": int(df["Views"].sum()),
        "Likes": int(df["Likes"].sum()),
        "Comments": int(df["Comments"].sum()),
        "Shares": int(df["Shares"].sum()),
        "Engagement Rate": "-"  # Engagement Rate is een gemiddelde, dus we laten dit leeg
    }
    return totals

# Streamlit interface
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Bernina Sans Condensed Extra Bold';
        src: url('https://raw.githubusercontent.com/RensvandenBerg224190/engagement-calculator/db7fd33f5020cc9d0a6b01d1769938a03fb9fb42/bernina-sans-condensed-extra-bold.otf') format('opentype');
    }

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Bernina Sans Condensed Extra Bold', sans-serif !important;
    }

    /* Normale tekst in Poppins */
    .stApp {
        background-color: #fbfaee;
        font-family: 'Poppins', sans-serif;
    }

    /* Secundaire kleur: #be95fd */
    .stButton button {
        background-color: #be95fd;
        color: black;
        font-weight: bold;
    }

    .stButton button:hover {
        background-color: white;
        color: #be95fd;
    }

    /* Stijlen voor de tabel */
    .stDataFrame thead th {
        background-color: #be95fd;
        color: #000000;  /* Zet de tekstkleur naar zwart */
        font-weight: bold;
    }

    .stDataFrame tbody td {
        color: black;
    }

    /* Logo grootte aanpassen */
    img[alt=""] {
        max-width: 100px !important;
        height: auto;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Voeg logo toe met aangepaste breedte
st.image(
    "https://raw.githubusercontent.com/RensvandenBerg224190/engagement-calculator/1dffaf3171c6aa00da8df075f6123d9640e2df16/PRIMARY-black.png",
    width=100  # Logo breedte aanpassen
)

st.title('TikTok Video Statistics')

# Gebruiker kan meerdere TikTok URL's invoeren
urls_input = st.text_area("Voer de TikTok video-URL's in, gescheiden door een nieuwe regel:", height=300)

if st.button("Verwerk URL's"):
    if urls_input:
        video_urls = urls_input.splitlines()
        videos = get_multiple_videos_data(video_urls)

        if videos:
            df = pd.DataFrame(videos)
            df = df.drop(columns=["Cover URL"])
            df['Engagement Rate'] = pd.to_numeric(df['Engagement Rate'], errors='coerce')
            df['Engagement Rate'].fillna(0, inplace=True)
            df['Engagement Rate (%)'] = df['Engagement Rate'].apply(lambda x: f"{round(x, 2)}%")
            df2 = df.drop(columns=["Engagement Rate"]).rename(columns={"Engagement Rate (%)": "Engagement Rate"})

            st.write("### Video Details")
            st.dataframe(df2)

            # Bereken totalen en gemiddelden
            totals = calculate_totals(df)
            averages = calculate_averages(df)

            totals_df = pd.DataFrame([totals])
            averages_df = pd.DataFrame([averages])

            # Verander de Engagement Rate naar een percentage weergave in averages
            averages_df["Engagement Rate (%)"] = averages_df["Engagement Rate"].apply(lambda x: f"{x}%")
            averages_df = averages_df.drop(columns=["Engagement Rate"]).rename(columns={"Engagement Rate (%)": "Engagement Rate"})
            
            totals2_df = totals_df.drop(columns=["Engagement Rate"])

            # Weergave van Total en Average Statistics naast elkaar
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Total Statistics")
                st.dataframe(totals2_df)
            with col2:
                st.write("### Average Statistics")
                st.dataframe(averages_df)
        else:
            st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
