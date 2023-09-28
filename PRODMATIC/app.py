from flask import Flask, render_template, request, redirect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from textblob import TextBlob
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


nltk.download('vader_lexicon')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviewapp.db'
db = SQLAlchemy(app)
app.app_context().push()
with app.app_context():
    db.create_all()

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    rev = db.Column(db.String(200))
    semantic = db.Column(db.Integer)
    link = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Review %r>' % self.id


@app.route('/', methods = ['POST','GET'])
def index():
    if request.method=="POST":
        tag = request.form.get("search")
        search = "%{}%".format(tag)
        reviews = Reviews.query.filter(Reviews.name.like(search)).all()
        return render_template('index.html', reviews=reviews)
    else: 
        
        reviews = Reviews.query.order_by(Reviews.date_created).all()
        return render_template('index.html', reviews=reviews)

@app.route('/delete/<int:id>')
def delete(id):
    rev_to_delete = Reviews.query.get_or_404(id)

    try:
        
        db.session.delete(rev_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/view/<int:idn>')
def view(idn):
    product = Reviews.query.order_by(Reviews.date_created).filter_by(id=idn).all()
    return render_template('view.html', review=product)


@app.route('/add_rev', methods = ['POST','GET'])
def add_rev():
    if request.method == "POST":
        inp = request.form.get("inp")
        rate = request.form.get("rate")
        name = request.form.get("name")
        link = request.form.get("link")
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(inp)
        #message = "Positive" if score['compound'] > 0 else "Negative" if score['compound'] < 0 else "Neutral"
        analysis = TextBlob(inp)
        sentiment = analysis.sentiment
        sentiment2 = score['compound']
        
        new_row = Reviews(name = name, rating = rate, rev = inp, semantic = sentiment2, link=link)
        db.session.add(new_row)
        db.session.commit()
        if score["compound"]>0:
            return render_template("add_rev.html",message="Positive",sentiment=sentiment,sentiment_score=score['compound'],input=inp, name=name, rate=rate)
        elif score["compound"]<0:
            return render_template("add_rev.html", message = "Negative",sentiment=sentiment,sentiment_score=score['compound'],input=inp, name=name, rate=rate)
        else:
            return render_template("add_rev.html", message = "Neutral",sentiment=sentiment,sentiment_score=0.0,input=inp, name=name, rate=rate)
    return render_template("add_rev.html")

@app.route('/filterdaa')
def filterdaa():
    reviews = Reviews.query.order_by(Reviews.date_created).all()
    return render_template('index.html', reviews=reviews)

@app.route('/filterdad')
def filterdad():
    reviews = Reviews.query.order_by(Reviews.date_created.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/filterrd')
def filterrd():
    reviews = Reviews.query.order_by(Reviews.rating.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/filterra')
def filterra():
    reviews = Reviews.query.order_by(Reviews.rating).all()
    return render_template('index.html', reviews=reviews)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)