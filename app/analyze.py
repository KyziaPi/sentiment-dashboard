# app/analyze.py
from textblob import TextBlob

def analyze_text(text):
    """
    Returns sentiment polarity:
    -1 (negative) to +1 (positive)
    """
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)
