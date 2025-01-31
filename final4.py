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
        "Views": df["Views"].mean(),
        "Likes": df["Likes"].mean(),
        "Comments": df["Comments"].mean(),
        "Shares": df["Shares"].mean(),
        "Engagement Rate": df["Engagement Rate"].mean()
    }
    return averages

# Streamlit interface
st.title('TikTok Video Statistics')

# Gebruiker kan meerdere TikTok URL's invoeren, gescheiden door nieuwe regels
urls_input = st.text_area(
    "Voer de TikTok video-URL's in, gescheiden door een nieuwe regel:",
    height=300
)

# Omzetten van de invoer naar een lijst van URL's
if urls_input:
    video_urls = urls_input.splitlines()

    # Verkrijg gegevens van de video's
    videos = get_multiple_videos_data(video_urls)

    if videos:
        # Maak een DataFrame om de gegevens in een tabel weer te geven (zonder de 'Cover URL' kolom)
        df = pd.DataFrame(videos)

        # Verwijder de 'Cover URL' kolom uit de tabel
        df = df.drop(columns=["Cover URL"])

        # Toon de tabel met video details (zonder 'Cover URL' kolom)
        st.write("### Video Details")
        st.dataframe(df)

        # Bereken de gemiddelde statistieken
        averages = calculate_averages(df)

        # Maak een DataFrame voor de gemiddelde waarden (zonder 'Username' kolom)
        averages_df = pd.DataFrame([averages])

        # Toon de tabel met de gemiddelde statistieken (zonder 'Username')
        st.write("### Average Statistics")
        st.dataframe(averages_df)

        # Toon de video covers als afbeeldingen
        for index, row in df.iterrows():
            cover_url = videos[index]["Cover URL"]
            if cover_url:
                st.write(f"### {row['Username']}")
                st.image(cover_url, width=200)  # Display de coverafbeelding

    else:
        st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
