from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import os


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.secret_key = "abcdefgh"
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    stocks = db.relationship('Stock', lazy=True)
    buyingPower = db.Column(db.Float)
    balance = db.Column(db.Float)
    def check_password(self, password):
        if self.password_hash == password:
            return True
        else:
            return False
    def get_id(self):
        return self.username
    def __repr__(self):
        return f"User('{self.username}','{self.password_hash}','{self.balance}','{self.buyingPower}')"
    

    

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(username=user_id).first()
class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(4096))
    purchasePrice = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return f"Stock('{self.symbol}','{self.purchasePrice}','{self.user}')"
class Helper():
    def getCurrentPrice(self):
        currentUserPrice = {}
        balance = 0
        user_stocks = Stock.query.filter_by(user=current_user.id).all()
        for stock in user_stocks:
            symbol = stock.symbol
            url = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch'
            headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
            page = requests.get(url, headers=headers)
            soup =  BeautifulSoup(page.content, 'html.parser')
            currentPrice = eval(soup.find('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).get_text())
            balance += currentPrice
            currentUserPrice[symbol] = currentPrice
        return currentUserPrice, balance

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html", error=False)
    user = load_user(request.form["username"])
    if user is None:
        return render_template("login.html", error=True)
    if not user.check_password(request.form["password"]):
        return render_template("login.html", error=True)
    login_user(user)
    return redirect(url_for('dash'))
    
@app.route("/Dash", methods=["GET", "POST"])
def dash():
    help = Helper()
    currentUserPrice = help.getCurrentPrice()[0]
    balance = help.getCurrentPrice()[1]
    user_stocks = Stock.query.filter_by(user=current_user.id).all()
    return render_template('/dashboard/dash.html', user = Users.query.filter_by(username=current_user.username).all(), user_stocks = Stock.query.filter_by(user=current_user.id).all(), currentUserPrice = currentUserPrice, balance = balance)

@app.route("/Orders", methods=["GET", "POST"])
def orders():
    help = Helper()
    currentUserPrice = help.getCurrentPrice()[0]
    balance = help.getCurrentPrice()[1]
    file = open('D:\\Stock App\symbols.txt', 'r')
    line = file.read().split(',')
    return render_template('orders.html', stocks=line, user_stocks = Stock.query.filter_by(user=current_user.id).all(), currentUserPrice = currentUserPrice, balance = balance)

@app.route('/purchase', methods=['POST'])
def purchase():
    symbol = request.form['symbol']
    currentUserPrice = {}
    url = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch'
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup =  BeautifulSoup(page.content, 'html.parser')
    currentPrice = eval(soup.find('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).get_text())
    shares = request.form['shares']
    current_user.buyingPower -= (currentPrice * float(shares))
    if request.method == 'POST':
        stock = Stock(symbol=symbol, purchasePrice=currentPrice, shares=shares, user=current_user.id)
        db.session.add(stock)
        db.session.commit()
    return redirect(url_for('orders'))

@app.route('/sell', methods=['POST'])
def sell():
    symbol = str(request.form['sellName'])
    symbol = symbol
    stock = Stock.query.filter_by(symbol=symbol, user=current_user.id).first()
    userShares = Stock.query.filter_by(symbol=symbol, user=current_user.id).first().shares
    sellShares = int(request.form['sellShares'])
    sellPrice = float(request.form['sellPrice'])
    balance = float(request.form['currBalance'])
    if userShares == sellShares:
        change = userShares * (sellPrice - Stock.query.filter_by(symbol=symbol, user=current_user.id).first().purchasePrice)
        current_user.buyingPower += abs(change)
        current_user.balance = balance
        stock = Stock.query.filter_by(symbol=symbol, user=current_user.id).first()
        db.session.delete(stock)
        db.session.commit()
        
    else:
        current_user.buyingPower += sellShares * sellPrice
        userShares -= sellShares
        stock.shares = userShares
        current_user.balance = balance
        db.session.commit()
    return redirect(url_for('dash'))





@app.route('/newUser', methods=['POST'])
def newUser():
    if request.method == 'POST':
        user = Users(username=request.form['new-user'], password_hash=request.form['pass'], balance=3000.00, buyingPower=3000.00)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    