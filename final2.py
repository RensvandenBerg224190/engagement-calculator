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

        return engagement_rate, likes, views, comments, shares
    else:
        print(f"De verwachte gegevens zijn niet gevonden voor video {video_url}")
        return None, 0, 0, 0, 0

# Functie om de gemiddelde engagement rate en statistieken te berekenen
def calculate_average_engagement_rate(video_urls):
    total_engagement = 0
    total_likes = 0
    total_views = 0
    total_comments = 0
    total_shares = 0
    count = 0

    for video_url in video_urls:
        video_id = video_url.split("/")[-1]  # Haal het video_id uit de URL
        engagement_rate, likes, views, comments, shares = calculate_engagement_rate(video_url, video_id)
        
        if engagement_rate is not None:
            total_engagement += engagement_rate
            total_likes += likes
            total_views += views
            total_comments += comments
            total_shares += shares
            count += 1

    # Bereken de gemiddelde engagement rate en statistieken
    if count > 0:
        average_engagement_rate = total_engagement / count
        average_likes = total_likes / count
        average_views = total_views / count
        average_comments = total_comments / count
        average_shares = total_shares / count
        return average_engagement_rate, average_likes, average_views, average_comments, average_shares
    else:
        return 0, 0, 0, 0, 0

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
        # Bereken de gemiddelde engagement rate en statistieken
        if st.button("Bereken Gemiddelde Engagement Rate"):
            average_engagement_rate, avg_likes, avg_views, avg_comments, avg_shares = calculate_average_engagement_rate(video_urls)

            if average_engagement_rate > 0:
                st.success(f"De gemiddelde engagement rate is: {average_engagement_rate:.2f}%")
                st.write(f"Gemiddeld aantal Likes: {avg_likes:.0f}")
                st.write(f"Gemiddeld aantal Views: {avg_views:.0f}")
                st.write(f"Gemiddeld aantal Comments: {avg_comments:.0f}")
                st.write(f"Gemiddeld aantal Shares: {avg_shares:.0f}")
            else:
                st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
