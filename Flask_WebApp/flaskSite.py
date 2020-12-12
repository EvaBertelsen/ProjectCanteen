from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, timedelta

cart = []

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="laznicka",
    password="*******",
    hostname="*****************",
    databasename="************",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = "cbhwecvwuebcwjkebcwuei"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    _tablename_ = "users"

    username = db.Column(db.String(128), primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Menu(db.Model):
    _tablename_ = "menu"

    name = db.Column(db.String(17), primary_key=True)
    alergens = db.Column(db.String(30))
    text = db.Column(db.String(50))
    price = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

#######################################################################################################################################
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("home.html", menu=Menu.query.all(), today = date.today(), yesterday = date.today() - timedelta(days=1))

@app.route("/logged/", methods=["GET", "POST"])
def mainl():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template("homel.html",  menu=Menu.query.all(), users=User.query.all(), today = date.today(), yesterday = date.today() - timedelta(days=1))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)
    username = request.form["username"]
    user = load_user(username)

    if user is None:
        return render_template("login_page.html", error=True)
    if not user.check_password(request.form["password"]):
        if username == "admin":
            return redirect(url_for('admin'))
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('mainl'))

@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=False)
    else:
        #id = request.form.get('id')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')

        new_user = User(username=username, password_hash=generate_password_hash(password), email=email, phone=phone)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('login'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("admin_page.html")
    else:
        name = request.form.get('name')
        alergens = request.form.get('alergens')
        text = request.form.get('text')
        price = request.form.get('price')
        date = request.form.get('date')

        new_item = Menu(name=name, alergens=alergens, text=text, price=price, date=date)

        db.session.add(new_item)
        db.session.commit()
        return redirect("admin_page.html", error=False)
    return redirect("admin_page.html")

