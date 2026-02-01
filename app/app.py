# app/app.py
import os
from flask import Flask, render_template, request
from fetch_api import get_news
from analyze import analyze_text
from datetime import datetime

# specify template folder relative to this file
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
app = Flask(__name__, template_folder=template_dir)

# helper to convert frontend datetime-local to ISO 8601 with Z
def to_iso8601_z(dt_str):
    """
    Convert datetime-local string (YYYY-MM-DDTHH:MM) to ISO 8601 with Z
    """
    if not dt_str:
        return None
    # add seconds if missing, then append Z
    dt = datetime.fromisoformat(dt_str)
    return dt.isoformat(timespec='seconds') + "Z"


@app.route("/", methods=["GET"])
def index():
    country = request.args.get("country", "us")
    from_date = to_iso8601_z(request.args.get("from_date"))
    to_date   = to_iso8601_z(request.args.get("to_date"))

    articles = get_news(country=country, from_date=from_date, to_date=to_date)

    results = []
    for article in articles:
        title = article.get("title", "")
        sentiment = analyze_text(title)
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

