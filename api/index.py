import time
import datetime as dt

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/longpoll')
def poll():
    t0=dt.datetime.now
    time.sleep(30)
    return(f"start:{t0}<br>I am polly now:{dt.datetime.now}")
