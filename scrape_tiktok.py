import http.client

conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "c5c5c7602cmshc5a01e9c18b6f4ep13e54fjsn05accb0124a7",
    'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
}

conn.request("GET", "/feed/search?keywords=fyp&region=nl&count=10&cursor=0&publish_time=1&sort_type=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))