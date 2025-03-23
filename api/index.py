import time
import datetime as dt
import json as JSON
import  logging, sys

from flask import Flask,request,render_template
logging.basicConfig(stream=sys.stdout,
level=logging.DEBUG,datefmt='%T %D',
format='%(asctime)s %(levelname)s %(message)s')

logger=logging.getLogger()

app = Flask(__name__)
app.config.update(
        TEMPLATES_AUTO_RELOAD=True
    )
app_command=""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/button',methods=['POST'])
def button():
    global app_command
    post=request.json
    event=post.get('event')
    btnindex=post.get('btnindex')
    name=post.get('name')
    logger.info("post event {} from button {}".format(event,name))
    data={"time":dt.datetime.now().isoformat(), "event":event, "name":name,"btnindex":btnindex}
    app_command=JSON.dumps(data)
    home()
    
@app.route('/about')
def about():
    return 'About<br>command proxy'

@app.route('/longpoll')
def poll():
    global app_command
    t0=dt.datetime.now().isoformat()
    ctr=0
    while app_command=="":
        time.sleep(0.2)
        ctr+=1
        if ctr>150:
            break
    apc_save=app_command
    app_command=""
    t1=dt.datetime.now().isoformat()
    data={"start":t0,"finish":t1,"pollcnt":ctr,"command":apc_save}
    return(JSON.dumps(data))
