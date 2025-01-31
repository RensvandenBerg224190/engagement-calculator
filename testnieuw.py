import requests

# TikTok video URL en video ID
video_url = "https://www.tiktok.com/@echo.nl/video/7464313077299711254"
video_id = "7464313077299711254"  # Vervang door de juiste video-id

# API URL en headers
url = "https://tiktok-scraper2.p.rapidapi.com/video/info_v2"
querystring = {"video_url": video_url, "video_id": video_id}

headers = {
    "X-RapidAPI-Key": "87f7d04a69msh064fc11c54bbcd5p1e1223jsn039442082ea2",  # Zorg ervoor dat je je API-sleutel gebruikt
    "X-RapidAPI-Host": "tiktok-scraper2.p.rapidapi.com"
}

# API-aanroep
response = requests.get(url, headers=headers, params=querystring)

# Checken of de respons succesvol is en de data printen
if response.status_code == 200:
    print("Succesvol data ontvangen:")
    print(response.json())  # Of gebruik response.text om het volledige antwoord te bekijken
else:
    print(f"Fout bij ophalen van data. Statuscode: {response.status_code}")
    print(response.text)
