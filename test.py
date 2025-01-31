import requests

video_id = "7464313077299711254"  # Vervang dit door een geldig TikTok video ID
url = f"https://www.tiktok.com/@echo.nl/video/7464313077299711254"

headers = {
    "X-RapidAPI-Key": "87f7d04a69msh064fc11c54bbcd5p1e1223jsn039442082ea2",  # Zorg ervoor dat je je API-sleutel gebruikt
    "X-RapidAPI-Host": "tiktok-scraper2.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

# Print de respons om te zien wat de fout precies is
print(response.status_code)
print(response.text)
