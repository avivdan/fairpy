# app.py
from flask import Flask, request, render_template, redirect, jsonify, url_for, flash

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rooms = request.form.get('rooms')
        rent = request.form.get('rent')

        if not rooms or not rent:
            flash('Please fill in the required fields')
            return redirect('/')
        else:
            # form is filled, do something
            pass

    return render_template('index.html')


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST' and request.form["rooms"] != '' and request.form["rent"] != '':
        rooms_input = int(request.form["rooms"])
        rent_input = int(request.form["rent"])
        return redirect(url_for("new_page", user_input=[rooms_input, rent_input]))
    return render_template('index.html')


@app.route("/table/<user_input>")
def new_page(user_input: str):
    print("user input ", user_input)
    print(type(user_input))
    s = ''
    res = []
    for i in user_input:
        if i != '[' and i != ']' and i != ',':
            s += i
        elif len(s) > 0:
            res.append(int(s))
            s = ''

    print(res)
    room = int(res[0])
    rent = int(res[1])
    return render_template("table.html", rooms=room, rents=rent)


@app.route("/home", methods=['POST'])
def home():
    print("yesss")
    return redirect(url_for("index"))

@app.route("/res", methods=['POST'])
def res():
    print("yesss")
    return redirect(url_for("result"))

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5001)
