# app/fetch_api.py
import requests

GNEWS_API_KEY = "39233749dff0f4e7fd41998ceb7f4838"
BASE_URL = "https://gnews.io/api/v4/top-headlines"


def get_news(country="us", max_articles=10, query=None, from_date=None, to_date=None):
    params = {
        "token": GNEWS_API_KEY,
        "lang": "en",
        "country": country,
        "max": max_articles,
        "q": query,
    }
    
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        # raise exception for bad HTTP codes
        response.raise_for_status()
        data = response.json()

        if "articles" not in data:
            return []

        articles = []
        for a in data.get("articles", []):
            articles.append({
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "")
            })

        return articles

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("GNews API daily limit reached!")
        else:
            print(f"HTTP error: {e}")
        return []

    except requests.exceptions.RequestException as e:
        # network error, DNS, timeout, etc
        print(f"Network/API error: {e}")
        return []
    
