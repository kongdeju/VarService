#! /usr/bin/env python
# coding: utf-8

import json
import os
from flask import Flask
from flask import request
from FiltVars import FiltVars,LoadVars,HeadVars
import  msgpack 
import json
import time
from modules.loads import hgmd_dict
from modules.hgmdservice.hgmd import hgmdserve
from modules.modeofinhere.add_genemode4vars import add_genemode

app = Flask('__name__')

#Trust_IP = ["127.0.0.1", "10.51.72.158","123.7.69.104"]


#@app.before_request
#def before_request():
#    if request.remote_addr not in Trust_IP:
#        return json.dumps({"status": "404", "message": "Page not accessible"})


@app.route('/ping/', methods=["GET"])
def ping():
    return "Service is online"

@app.route("/filter/<sample_no>/", methods=["GET","POST"])
def filt_vars(sample_no):
    try:
        request_data = json.loads(request.data)
        filt_str = request_data["filt"]
        rec_time = time.ctime()
        filt_log = rec_time + "\t" + filt_str + "\n"
        os.system('echo "%s" >>filt.log' % filt_log)
    except Exception as e:
        filt_str = "All"
    Status,Vars = FiltVars(sample_no,filt_str)
    Vars = add_genemode(Vars)
    return json.dumps({"status":Status,"vars":Vars})

@app.route("/get/<sample_no>/",methods=["GET","POST"])
def get_vars(sample_no):
    Status,Vars = LoadVars(sample_no)
    Vars = add_genemode(Vars)
    return json.dumps({"status":Status,"vars":Vars})

@app.route("/head/<sample_no>/",methods=["GET","POST"])
def head_vars(sample_no):
    Status,Vars = HeadVars(sample_no)
    Vars = add_genemode(Vars)
    return json.dumps({"status":Status,"vars":Vars})

@app.route("/hgmd/<hgmdid>/",methods=["get"])
def get_hgmd(hgmdid):
    rec = hgmdserve(hgmdid,hgmd_dict)
    return rec


@app.route("/wakeup/",methods=["GET","POST"])
def wake():
    time.sleep(2)
    return "I am awake"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
