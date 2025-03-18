from flask import Flask
from flask import render_template, request
import json
import logging,sys
import subprocess
import os
import datetime as dt
import time

app=Flask(__name__)
#logging.basicConfig(stream=sys.stdout,
#    level=logging.DEBUG,datefmt='%T %D',
#    format='%(asctime)s %(levelname)s %(message)s')
#logger=logging.getLogger()
#logger.info("Flask app created")

@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/poll')
def long_poll():
    client_state = {"dog":"cat","frienchip":10}
    #request.args.get("state")

    #poll the database
    while True:
        time.sleep(30)
        data = {"dog":"cat","frienchip":30}
        json_state = json.dumps(data)
        #json_state = "".join(data) #remove whitespace

        if json_state != client_state:
            return "CHANGE"

@app.route('/config')
def get_config():
    return json.dumps(app.screens)



@app.route('/about')
def about():
    return 'About'

@app.route('/button',methods=['POST'])
def button():
    post=request.json
    event=post.get('event')
    btnindex=post.get('btnindex')
    name=post.get('name')
    logger.info("post event {} from button {}".format(event,name))
    if event=="touch start":
        cmd=msghandler(btnindex=btnindex, buttonconfig=app.buttons,templateconfig=app.cmdtemplates)
        if cmd!="":
            execute(cmd)
            return "Post - OK."
        else:
            return "Post - Empty command"
    else:
        return "unhandled"

def msghandler(btnindex,buttonconfig,templateconfig):
    btns=buttonconfig
    btn=btns[btnindex]
    tmpl=btn.get('tmp')
    if tmpl is None:
        tmpl=buttonconfig.get('tmp')
        btn['tmp']=tmpl
    logger.info("btn config:{}".format(btn))
    template=templateconfig[tmpl]
    if btn.get('code'):
        cmd=template.format(msg=btn['code'])
    else:
        cmd=""
    return cmd

def execute(cmd):
    logger.info("executing  shell command:{}".format(cmd))
    result=subprocess.call(cmd,shell=True,timeout=2)
    logger.info("result from shell command:{}".format(result))
    return(result)
