
### From the console> pip3 install flask

from flask import Flask, render_template

#import sqlite3

#conn = sqlite3.connect('example.db')


app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template("mainpage.html")

@app.route('/Beverages & Desserts')
def Beverages & Desserts():
    return render_template("other.html")


@app.route('/Orders/')
def orders():
    return render_template("orders.html")

@app.route('/My Account/')
def myaccount():
    return render_template("myaccount.html")


if __name__ == "__main__":
    app.run(debug=True)


# Eva added pages