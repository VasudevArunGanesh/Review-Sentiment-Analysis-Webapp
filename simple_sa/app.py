from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from textblob import TextBlob


nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == "POST":
        inp = request.form.get("inp")
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(inp)
        #message = "Positive" if score['compound'] > 0 else "Negative" if score['compound'] < 0 else "Neutral"
        analysis = TextBlob(inp)
        sentiment = analysis.sentiment
        if score["compound"]>0:
            return render_template('index.html',message="Positive",sentiment=sentiment,sentiment_score=score['compound'],input=inp)
        elif score["compound"]<0:
            return render_template('index.html', message = "Negative",sentiment=sentiment,sentiment_score=score['compound'],input=inp)
        else:
            return render_template('index.html', message = "Neutral",sentiment=sentiment,sentiment_score=0.0,input=inp)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)