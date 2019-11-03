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

@app.route("/search", methods = ["GET", "POST"])
def search():
    Questions = ["Question"]
    Points = ["Points"]
    Answers = ["Answer"]
    Categories = ["Category"]
    Airdates = ["Air Date"]
    keyword = 'base'
    information = ""
    if request.method == "POST" and request.form['submit'] == 'Find':
        keyword = request.form['keyword']
        maxCount = request.form['maxCount']
        information = get("http://jservice.io/api/random?count=" + maxCount)
        Questions = ["Question"]
        Points = ["Points"]
        Answers = ["Answer"]
        Categories = ["Category"]
        Airdates = ["Air Date"]
        for index in range(0, int(maxCount)):
            Categories.append(information[index]["category_id"])
            Questions.append(information[index]["question"])
            Points.append(information[index]["value"])
            Answers.append(information[index]["answer"])
            Airdates.append(information[index]["airdate"][0:10])
    return render_template("search.html", searched = keyword, airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))

@app.route("/favorites")
def favorites():
    return render_template('favorites.html', title='Favorites')

if __name__ == '__main__':
    app.run(debug=True)
