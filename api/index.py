import time
import datetime as dt
import json as JSON
import  logging, sys
from collections import Counter

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
    data={"receive_time":dt.datetime.now().isoformat(), "event":event, "name":name,"btnindex":str(btnindex)}
    app_command=JSON.dumps(data)
    return home()

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
    if apc_save!="":
        command=JSON.loads(apc_save)
        logger.info(JSON.dumps(command))
        data0={"start":t0, "finish":t1, "pollcnt":str(ctr), "commands":"True"}
        logger.info(JSON.dumps(data0))
        data= {i: command.get(i, "") + data0.get(i, "") 
                for i in set(command).union(data0)}
    else:
        data ={"start":t0, "finish":t1, "pollcnt":str(ctr), "commands":"False"}
    return(JSON.dumps(data))

def create_app_for_test(appcommand):
    global app_command
    app = Flask(__name__)
    app.config.update(
            TEMPLATES_AUTO_RELOAD=True
        )
    app_command=appcommand
    return app