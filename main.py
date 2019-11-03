import requests
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search", methods = ["GET", "POST"])
def search():
    Questions = ["Questions"]
    Points = ["Points"]
    Answers = ["Answer"]
    keyword = 'base'
    information = ""
    if request.method == "POST":
        keyword = request.form['keyword']
        information = get("http://jservice.io/api/random?count=10")
        Questions = ["Questions"]
        Points = ["Points"]
        Answers = ["Answer"]
        for index in range(0, len(information)):
            Questions.append(information[index]["question"])
            Points.append(information[index]["value"])
            Answers.append(information[index]["answer"])
    return render_template("search.html", searched = keyword, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))

@app.route("/favorites")
def favorites():
    return render_template('favorites.html', title='Favorites')

if __name__ == '__main__':
    app.run(debug=True)
