# app/app.py
from flask import Flask, render_template
from fetch_api import get_data
from analyze import analyze_text

app = Flask(__name__)

@app.route("/")
def index():
    articles = get_data()
    results = []

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        # analyze title + description
        text_to_analyze = title if title else description
        sentiment_score = analyze_text(text_to_analyze)
        results.append({
            "title": title,
            "description": description,
            "sentiment": sentiment_score
        })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

