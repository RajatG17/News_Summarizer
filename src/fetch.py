## Fetcher toget top headlines from newsapi.org
import os
import requests

# Set api key and fetch URL

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise ValueError("Please set the NEWSAPI_KEY environment variable.")
else:
    print("API key loaded successfully.")
    
BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_top_headlines(country="us", category="technology", page_size=10, keywords=None):
    """
    Fetch top headlines from NewsAPI.
    
    Args:
        country : country code
        category : news category
        page_size : number of articles to fetch
        keywords : keywords to filter articles
        
    Returns:
        list of dicts: {"title": str, "url":str"}
    """
    params = {
        "apiKey": NEWSAPI_KEY,
        "country": country, 
        "pageSize": page_size
    }

    if category:
        params["category"] = category
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status() # raises an HTTPError if the response was unsuccessful
    data = response.json()
    articles = data.get("articles", [])
    items = [{"title": a["title"], "url": a["url"]} for a in articles]
    if keywords:
        items = [item for item in items if any(keyword.lower() in item["title"].lower() for keyword in keywords)]
    return normalize_headlines(items)


def normalize_headlines(headlines):
    """
    Normalize the headlines to a standard format and remove duplicates.
    
    Args:
        headlines: list of dicts
    returns:
        list of dicts: {"title": str, "url":str"}
    """
    seen = set()
    unique = []
    for item in headlines:
        title = item["title"].strip()
        if title and title not in seen:
            seen.add(title)
            unique.append({
                "title": title,
                "url": item["url"]
            })
    return unique


# url = "https://newsapi.org/v2/top-headlines"
# params = {"apiKey": os.getenv("NEWSAPI_KEY"), "country": "us", "pageSize": 10, "cateory": "technology" }
# resp = requests.get(url, params=params)
# headlines = [{"title":e.title, "url": e.link} for e in resp.["articles"]]
