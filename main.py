import requests
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

FavoriteQuestions = ["Question"]
FavoriteCategories = ["Category"]
FavoritePoints = ["Points"]
FavoriteAnswers = ["Answer"]
FavoriteAirdates = ["Airdate"]

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
    if request.method == "POST" and request.form['submit'] == 'Find':
        Questions = ["Question"]
        Points = ["Points"]
        Answers = ["Answer"]
        Categories = ["Category"]
        Airdates = ["Air Date"]
        information = ""
        queryString = ""
        minAirdate = ""
        maxAirdate = ""
        maxCount = request.form['maxCount']
        keyword = request.form['keyword']
        difficulty = request.form['difficulty']
        category = request.form['category']
        minAirdate = request.form['minAirdate']
        maxAirdate = request.form['maxAirdate']

        count = 0
        index = 0
        queryString = "?"
        if difficulty != "":
            queryString = queryString + "&value=" + difficulty
        if minAirdate != "":
            queryString = queryString + "&min_date=" + minAirdate
        if maxAirdate != "":
            queryString = queryString + "&max_date=" + maxAirdate
        if category != "":
            categoryID = 0
            offsetCount = 0
            while categoryID == 0:
                categoryInfo = get("http://jservice.io/api/categories?count=100&offset=" + str(offsetCount))
                if categoryInfo == []:
                    categoryID = -1
                else:
                    for categoryIndex in range(0,len(categoryInfo)):
                        if str(categoryInfo[categoryIndex]["title"]).lower() == category.lower():
                            categoryID = categoryInfo[categoryIndex]["id"]
                    offsetCount+=100
            queryString = queryString + "&category=" + str(categoryID)


        queryString = "http://jservice.io/api/clues" + queryString + "&offset="
        offsetSearch = 0
        information = get(queryString+str(offsetSearch))
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
            if keyword != "":
                keySearchText = str(information[index])
                if keySearchText.lower().find(keyword.lower()) != -1 and information[index]["question"] != "":
                    Categories.append(information[index]["category"]["title"])
                    Questions.append(information[index]["question"])
                    Points.append(information[index]["value"])
                    Answers.append(information[index]["answer"])
                    Airdates.append(information[index]["airdate"][0:10])

                    count+=1
            else:
                if information[index]["question"] != "":
                    Categories.append(information[index]["category"]["title"])
                    Questions.append(information[index]["question"])
                    Points.append(information[index]["value"])
                    Answers.append(information[index]["answer"])
                    Airdates.append(information[index]["airdate"][0:10])
                    count+=1
            index+=1
            if index >= len(information):
                index=0
                offsetSearch+=100
                information = get(queryString+str(offsetSearch))
                if information == []:
                    return render_template("search.html", airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))
    elif request.method == "POST":
        FavoriteQuestions.append(request.form["questionEntry"])
        FavoriteCategories.append(request.form["categoryEntry"])
        FavoriteAnswers.append(request.form["answerEntry"])
        FavoriteAirdates.append(request.form["airdateEntry"])
        FavoritePoints.append(request.form["pointEntry"])
        return '', 204
    else:
        Questions = ["Question"]
        Points = ["Points"]
        Answers = ["Answer"]
        Categories = ["Category"]
        Airdates = ["Air Date"]
    return render_template("search.html", airdates = Airdates, categories = Categories, questions = Questions, points = Points, answers = Answers, title = 'Search', len = len(Questions))


@app.route("/favorites", methods = ['GET','POST'])
def favorites():
    if request.method == "POST" and request.form['submit'] == 'Remove':
        FavoriteQuestions.remove(request.form["fquestionEntry"])
        FavoriteAirdates.remove(request.form["fairdateEntry"])
        FavoritePoints.remove(request.form["fpointEntry"])
        FavoriteAnswers.remove(request.form["fanswerEntry"])
        FavoriteCategories.remove(request.form["fcategoryEntry"])
    return render_template("favorites.html", airdates = FavoriteAirdates, categories = FavoriteCategories, questions = FavoriteQuestions, points = FavoritePoints, answers = FavoriteAnswers, title = 'Favorites', len = len(FavoriteQuestions))

if __name__ == '__main__':
    app.run(debug=True)

