import streamlit as st
import requests

# Functie om engagement rate voor een enkele TikTok video te berekenen
def calculate_engagement_rate(video_url, video_id):
    url = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
    querystring = {"video_url": video_url, "video_id": video_id}

    headers = {
        "x-rapidapi-key": "87f7d04a69msh064fc11c54bbcd5p1e1223jsn039442082ea2",
        "x-rapidapi-host": "tiktok-scraper2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # Haal de JSON-gegevens op
    data = response.json()

    # Zorg ervoor dat de 'itemInfo' en 'itemStruct' aanwezig zijn in de response
    if 'itemInfo' in data and 'itemStruct' in data['itemInfo']:
        item = data['itemInfo']['itemStruct']
        
        # Haal de statistieken op
        stats = item.get('stats', {})

        # Verkrijg de gewenste statistieken, als deze aanwezig zijn
        likes = stats.get("diggCount", 0)
        views = stats.get("playCount", 0)
        comments = stats.get("commentCount", 0)
        shares = stats.get("shareCount", 0)

        # Bereken de engagement rate (als views groter dan 0 zijn om deling door 0 te voorkomen)
        if views > 0:
            engagement_rate = ((likes + comments + shares) / views) * 100
        else:
            engagement_rate = 0

        return engagement_rate
    else:
        print(f"De verwachte gegevens zijn niet gevonden voor video {video_url}")
        return None

# Functie om de gemiddelde engagement rate te berekenen
def calculate_average_engagement_rate(video_urls):
    total_engagement = 0
    count = 0

    for video_url in video_urls:
        video_id = video_url.split("/")[-1]  # Haal het video_id uit de URL
        engagement_rate = calculate_engagement_rate(video_url, video_id)
        
        if engagement_rate is not None:
            total_engagement += engagement_rate
            count += 1

    # Bereken de gemiddelde engagement rate
    if count > 0:
        average_engagement_rate = total_engagement / count
        return average_engagement_rate
    else:
        return 0

# Streamlit interface
st.title('TikTok Engagement Rate Calculator')

# Gebruiker kan meerdere TikTok URL's invoeren, max 50
urls_input = st.text_area(
    "Voer de TikTok video-URL's in, gescheiden door een nieuwe regel (max 50 URLs):",
    height=300
)

# Omzetten van de invoer naar een lijst van URL's
if urls_input:
    video_urls = urls_input.splitlines()

    # Zorg ervoor dat het aantal URL's niet groter is dan 50
    if len(video_urls) > 50:
        st.error("Je kunt maximaal 50 URL's invoeren.")
    else:
        # Bereken de gemiddelde engagement rate
        if st.button("Bereken Gemiddelde Engagement Rate"):
            average_engagement_rate = calculate_average_engagement_rate(video_urls)

            if average_engagement_rate > 0:
                st.success(f"De gemiddelde engagement rate is: {average_engagement_rate:.2f}%")
            else:
                st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
