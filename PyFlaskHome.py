#http://diamondinternational.org/
print('Website Is Live')

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
# added for postgre DB
import psycopg2
import psycopg2.extras
import pytz
# import pandas_market_calendars as MarketDays
# from datetime import date, timedelta, datetime
from passwords import passpee
key1,dbname1,user1,password1,host1 = passpee()
app = Flask(__name__)
app.secret_key = key1

def is_authenticated():
    return 'authenticated' in session
@app.route("/Signin", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])

def SignIn():
    if request.method == "POST":
        key = request.form['secret_key']
        if key == app.secret_key:
            session['authenticated'] = True
            return redirect(url_for('Account'))
        else:
            return render_template('signin.html', error="Wrong password!!!")
    return render_template('signin.html')

@app.route("/Account")
def Account():
    if session['authenticated'] == True:

        return render_template('account.html')
    return render_template('signin.html')
        
@app.route("/Settings")
def settings():
    if session['authenticated'] == True:
        return render_template('settings.html')
    return render_template('signin.html')

@app.route('/Metals')
def callGarage():
    if session['authenticated'] == True:
        return render_template('metals.html')
    return render_template('signin.html')


@app.route('/Crypto')
def CallBackYard():
    if session['authenticated'] == True:
        return render_template('crypto.html')
    return render_template('signin.html')


@app.route('/Bonds')
def CallFrontYard():
    if session['authenticated'] == True:
        return render_template('bonds.html')
    return render_template('signin.html')

@app.route("/Trades")
def playground():

    if session['authenticated'] == True:
        # added for postgre DB

        con = psycopg2.connect(dbname=dbname1, user=user1, password=password1, host=host1)
        curr = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curr.execute("SELECT * FROM StockInfo1")

        rows = curr.fetchall()
        con.commit()

        return render_template('trades.html', rows=rows)
    return render_template('signin.html')



# --------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8080)