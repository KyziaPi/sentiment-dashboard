# app/fetch_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_data():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Status code:", response.status_code)
        articles = response.json().get("articles", [])
        print("Articles fetched:", len(articles))
        return articles[:10]
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []

