from flask import Flask,redirect,request
import random

app = Flask("__name__")

clients = ["10.44.147.219:8001","10.51.75.12:8001"]

num = len(clients)
i = 0

def choose():
	global i
	i = i + 1
	mod = i % num 
	return mod

@app.route("/wakeup/",methods=["GET","POST"])
def wake():
	i = choose()
	url = "http://%s/wakeup/" % clients[i]
	return redirect(url,code=307)

@app.route("/filter/<sample_no>/",methods=["GET","POST"])
def filt_vars(sample_no):
	i = choose()
	url = "http://%s/filter/%s/" % (clients[i],sample_no)
	return redirect(url,code=307)

@app.route("/get/<sample_no>/",methods=["GET","POST"])
def get_vars(sample_no):
	i = choose()
	url = "http://%s/get/%s/" % (clients[i],sample_no)
	return redirect(url,code=307)

@app.route("/head/<sample_no>/",methods=["GET","POST"])
def head_vars(sample_no):
	i = choose()
	url = "http://%s/head/%s/" % (clients[i],sample_no)
	return redirect(url,code=307)

@app.route("/hgmd/<variant_id>/",methods=["GET","POST"])
def hgmd_vars(variant_id):
	i = choose()
	url = "http://%s/hgmd/%s/" % (clients[i],variant_id)
	return redirect(url,code=307)


if __name__ == "__main__":
	app.run(debug=True)
