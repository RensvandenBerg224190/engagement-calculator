import requests
import pandas as pd
import streamlit as st

# Functie om gegevens van een TikTok-video op te halen
def get_video_data(video_url, video_id):
    url = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
    querystring = {"video_url": video_url, "video_id": video_id}

    headers = {
        "x-rapidapi-key": "87f7d04a69msh064fc11c54bbcd5p1e1223jsn039442082ea2",
        "x-rapidapi-host": "tiktok-scraper2.p.rapidapi.com"
    }

    # Verstuur het verzoek naar de API
    response = requests.get(url, headers=headers, params=querystring)

    # Haal de JSON-gegevens op
    data = response.json()

    # Controleer of de verwachte gegevens aanwezig zijn
    if 'itemInfo' in data and 'itemStruct' in data['itemInfo']:
        item = data['itemInfo']['itemStruct']
        
        # Verkrijg de username van de auteur
        username = item.get('author', {}).get('uniqueId', 'Onbekend')
        
        # Haal de cover URL uit de JSON-gegevens
        cover_url = item.get("video", {}).get("cover", "")
        
        # Haal de statistieken op
        stats = item.get('stats', {})

        # Verkrijg de gewenste statistieken
        likes = stats.get("diggCount", 0)
        views = stats.get("playCount", 0)
        comments = stats.get("commentCount", 0)
        shares = stats.get("shareCount", 0)

        # Bereken de engagement rate (als views groter dan 0 zijn om deling door 0 te voorkomen)
        if views > 0:
            engagement_rate = ((likes + comments + shares) / views) * 100
        else:
            engagement_rate = 0

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
        video_id = video_url.split("/")[-1]  # Haal het video_id uit de URL
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

# Streamlit interface
st.title('TikTok Video Statistics')

# Gebruiker kan meerdere TikTok URL's invoeren, gescheiden door nieuwe regels
urls_input = st.text_area(
    "Voer de TikTok video-URL's in, gescheiden door een nieuwe regel:",
    height=300
)

# Voeg een knop toe die de gegevens ophaalt bij klikken
if st.button("Verwerk URL's"):
    if urls_input:
        video_urls = urls_input.splitlines()

        # Verkrijg gegevens van de video's
        videos = get_multiple_videos_data(video_urls)

        if videos:
            # Maak een DataFrame om de gegevens in een tabel weer te geven (zonder de 'Cover URL' kolom)
            df = pd.DataFrame(videos)

            # Verwijder de 'Cover URL' kolom uit de tabel
            df = df.drop(columns=["Cover URL"])

            # Zet de 'Engagement Rate' kolom om naar numeriek, vervang niet-numerieke waarden door NaN
            df['Engagement Rate'] = pd.to_numeric(df['Engagement Rate'], errors='coerce')

            # Vervang NaN-waarden door 0
            df['Engagement Rate'].fillna(0, inplace=True)

            # Bewaar de originele Engagement Rate zonder '%' voor de berekening, en voeg '%' toe in de weergave
            df['Engagement Rate (%)'] = df['Engagement Rate'].apply(lambda x: f"{round(x, 2)}%")  # Afronden naar 2 decimalen met '%' toegevoegd
            
            # Maak een kopie van df zonder de 'Engagement Rate' kolom
            df2 = df.drop(columns=["Engagement Rate"])

            # Hernoem de kolom 'Engagement Rate (%)' naar 'Engagement Rate' in df2
            df2 = df2.rename(columns={"Engagement Rate (%)": "Engagement Rate"})
            
            # Toon de tabel met video details (zonder 'Cover URL' kolom)
            st.write("### Video Details")
            st.dataframe(df2)

            # Bereken de gemiddelde statistieken
            averages = calculate_averages(df)

            # Maak een DataFrame voor de gemiddelde waarden
            averages_df = pd.DataFrame([averages])

            # Zet de 'Engagement Rate' in de gemiddelde tabel om naar een percentage string (met '%')
            averages_df["Engagement Rate (%)"] = averages_df["Engagement Rate"].apply(lambda x: f"{x}%")  # '% toevoegen

            # Verwijder de originele "Engagement Rate" kolom zonder % van de gemiddelde tabel
            averages_df = averages_df.drop(columns=["Engagement Rate"])

            # Hernoem de kolom 'Engagement Rate (%)' naar 'Engagement Rate' in averages
            averages_df = averages_df.rename(columns={"Engagement Rate (%)": "Engagement Rate"})

            # Toon de tabel met de gemiddelde statistieken
            st.write("### Average Statistics")
            st.dataframe(averages_df)

#            # Toon de video covers als afbeeldingen
#            for index, row in df.iterrows():
#                cover_url = videos[index]["Cover URL"]
#                if cover_url:
#                    st.write(f"### {row['Username']}")
#                    st.image(cover_url, width=200)  # Display de coverafbeelding

        else:
            st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
