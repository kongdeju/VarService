#! /usr/bin/env python
# coding: utf-8

import json
import os
from flask import Flask
from flask import request
from FiltVars import FiltVars,LoadVars,HeadVars
#import  msgpack 
import json
import time
from modules.loads import hgmd_dict
from modules.hgmdservice.hgmd import hgmdserve


app = Flask('__name__')

#Trust_IP = ["127.0.0.1", "10.51.72.158","123.7.69.104"]


#@app.before_request
#def before_request():
#    if request.remote_addr not in Trust_IP:
#        return json.dumps({"status": "404", "message": "Page not accessible"})


@app.route('/ping/', methods=["GET"])
def ping():
    return "Service is online"

@app.route("/filter/<sample_no>/", methods=["GET"])
def filt_vars(sample_no):
	try:
		request_data = json.loads(request.data)
		filt_str = request_data["filt"]
	except Exception as e:
		filt_str = "All"
	Status,Vars = FiltVars(sample_no,filt_str)
	return json.dumps({"status":Status,"vars":Vars})
	return "error"

@app.route("/get/<sample_no>/",methods=["GET"])
def get_vars(sample_no):
	Status,Vars = LoadVars(sample_no)
	return json.dumps({"status":Status,"vars":Vars})

@app.route("/head/<sample_no>/",methods=["GET"])
def head_vars(sample_no):
	Status,Vars = HeadVars(sample_no)
	return json.dumps({"status":Status,"vars":Vars})

@app.route("/hgmd/<id>/",methods=["get"])
def get_hgmd(id):
	rec = hgmdserve(id,hgmd_dict)
	return rec


@app.route("/wakeup/",methods=["GET"])
def wake():
	time.sleep(1)
	return "I am awake"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
