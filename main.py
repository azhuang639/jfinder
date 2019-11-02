from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search", methods = ["GET", "POST"])
def search():
    keyword = 'base'
    if request.method == "POST":
        keyword = request.form['keyword']
    return render_template("search.html", searched = keyword)

if __name__ == '__main__':
    app.run(debug=True)