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
    return render_template('home.html', title='Home', homepage = True)

@app.route("/search", methods = ["GET", "POST"])
def search():
    Questions = ["Question"]
    Points = ["Points"]
    Answers = ["Answer"]
    Categories = ["Category"]
    Airdates = ["Air Date"]
    keyword = 'base'
    information = ""
    queryString = ""
    if request.method == "POST" and request.form['submit'] == 'Find':
        maxCount = request.form['maxCount']
        keyword = request.form['keyword']
        difficulty = request.form['difficulty']
        category = request.form['category']

        Questions = ["Question"]
        Points = ["Value"]
        Answers = ["Answer"]
        Categories = ["Category"]
        Airdates = ["Air Date"]
        count = 0
        index = 0
        #if False:#keyword != "":
        #    if maxCount == "":
        #        maxCount = 10
        #    while count < maxCount:
        #        information = get("http://jservice.io/api/clues?")
        #else:
        queryString = "?"
        if difficulty != "":
            queryString = queryString + "&value=" + difficulty
        if category != "":
            categoryID = 0;
            offsetCount = 0;
            while categoryID == 0:
                categoryInfo = get("http://jservice.io/api/categories?count=100&offest=" + offsetCount)
                if categoryInfo == []:
                    categoryID = -1
                for categoryIndex in range(0,len(categoryInfo)):
                    if categoryInfo[categoryIndex]["title"].lower() == category.lower():
                        categoryID = categoryInfo[categoryIndex]["id"]
                offsetCount+=100
            queryString = queryString + "&category=" + categoryID


        queryString = "http://jservice.io/api/clues" + queryString
        information = get(queryString)
        if maxCount == "":
            maxCount = 0
        maxCount = min(int(maxCount), len(information))
        while count < maxCount:
                #if keyword != "":
                #    keySearchText = str(information[index])
                #    while keySearchText.lower().find(keyword.lower()) == -1:
                #        index+=1
                #        if index >= len(information):
                #            return render_template("search.html", searched = keyword, airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))
                #        keySearchText = str(information[index])
            Categories.append(information[index]["category"]["title"])
            Questions.append(information[index]["question"])
            Points.append(information[index]["value"])
            Answers.append(information[index]["answer"])
            Airdates.append(information[index]["airdate"][0:10])
            index+=1
            count+=1
            if index >= len(information):
                return render_template("search.html", searched = keyword, airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))
    return render_template("search.html", airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))

@app.route("/favorites")
def favorites():
    return render_template('favorites.html', title='Favorites')

if __name__ == '__main__':
    app.run(debug=True)
