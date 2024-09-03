from textblob import TextBlob
def sentimentAnalysis(text):
    blob = TextBlob(text)

    score = blob.sentiment.polarity

    if score <= -1.0:
        return "Very Negative"
    elif score <= -0.8:
        return "Negative"
    elif score <= -0.6:
        return "Somewhat Negative"
    elif score <= -0.4:
        return "Slightly Negative"
    elif score <= 0.0:
        return "Neutral"
    elif score <= 0.4:
        return "Slightly Positive"
    elif score <= 0.6:
        return "Somewhat Positive"
    elif score <= 0.8:
        return "Positive"

    return "Very Positive"
    
