# app/fetch_api.py
import requests
from textblob import TextBlob

GNEWS_API_KEY = "42c2e0c4a28110fd8c679a8bbc15ac21"

def get_news(country="us", max_articles=10, query=None, category=None, from_date=None, to_date=None):
    q_clean = query.strip() if query and query.strip() else None
    cat_clean = category.strip() if category and category.strip() else None
    
    params = {
        "token": GNEWS_API_KEY,
        "lang": "en",
        "country": country if country else "us",
        "max": max_articles,
    }

    if q_clean:
        url = "https://gnews.io/api/v4/search"
        # Search endpoint ignores 'category' merge into search string
        params["q"] = f'"{q_clean}" {cat_clean}' if cat_clean else q_clean
    else:
        url = "https://gnews.io/api/v4/top-headlines"
        params["category"] = cat_clean if cat_clean else "general"

    if from_date: params["from"] = from_date
    if to_date:   params["to"] = to_date

    try:
        print(f"\n--- ATTEMPTING FETCH ---")
        print(f"URL: {url}")
        print(f"Final Params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for a in data.get("articles", []):
            text = f"{a.get('title', '')} {a.get('description', '')}"
            score = round(TextBlob(text).sentiment.polarity, 2)
            articles.append({
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", ""),
                "sentiment": score
            })
        print(f"Success: Found {len(articles)} articles.")
        return articles
    except Exception as e:
        print(f"API Error: {e}")
        return []