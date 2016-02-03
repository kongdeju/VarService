from fabric.api import *

env.hosts = ["Varer@10.44.147.219:22"]

env.roledefs = {"api":["Varer@10.44.147.219:22"]}


def update_clients():
    with cd('/data/vars_project/vars_service/'):
        run('git fetch')
        run('git reset --hard origin/master')

def stop_clients():
	with cd('/data/vars_project/vars_service/'):
		run('sh stop.sh')
def start_clients():
	with cd('/data/vars_project/vars_service/'):
		run('sh run.sh && sleep 1')

@roles("api")
def stop_api():
	with cd('/data/vars_project/vars_service/interface/'):
		run('sh stop.sh')

@roles("api")
def start_api():
	with cd('/data/vars_project/vars_service/interface/'):
		run('sh -x run.sh && sleep 1')
