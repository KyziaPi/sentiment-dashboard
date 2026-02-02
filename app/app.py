# app/app.py
import os
from flask import Flask, render_template, request
from fetch_api import get_news
from analyze import analyze_text
from datetime import datetime

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
app = Flask(__name__, template_folder=template_dir)

def to_iso8601_z(dt_str):
    if not dt_str:
        return None
    dt = datetime.fromisoformat(dt_str)
    return dt.isoformat(timespec='seconds') + "Z"

@app.route("/", methods=["GET"])
def index():
    # --- FIX: grab from browser ---
    query = request.args.get("q", "")           
    category = request.args.get("category", "") 
    country = request.args.get("country", "ph")
    
    from_date = to_iso8601_z(request.args.get("from_date"))
    to_date   = to_iso8601_z(request.args.get("to_date"))

    # --- FIX: Passing query and category into the function ---
    articles = get_news(
        query=query, 
        category=category, 
        country=country, 
        from_date=from_date, 
        to_date=to_date
    )

    results = []
    for article in articles:
        title = article.get("title", "")
        sentiment = article.get("sentiment", 0) 
        results.append({
            "title": title,
            "description": article.get("description", ""),
            "source": article.get("source", ""),
            "sentiment": sentiment,
            "url": article.get("url", "")
        })

    return render_template("index.html", results=results, country=country)

if __name__ == "__main__":
    app.run(debug=True)
