from fabric.api import *

env.hosts = ["Varer@10.44.147.219:22"]

env.roledefs = {"api":["Varer@10.44.147.219:22"]}


def update_clients():
    with cd('/data/vars_project/vars_service/'):
        run('git fetch')
        run('git reset --hard origin/master')

def restart_clients():
	with cd('/data/vars_project/vars_service/'):
		run('sh stop.sh')
		run('sh run.sh')

def stop_clients():
	with cd('/data/vars_project/vars_service/'):
		run('sh stop.sh')

@roles("api")
def restart_interface():
	with cd('/data/vars_project/vars_service/interface/'):
		run('sh stop.sh')
		run('sh run.sh')

@roles("api")
def stop_interface():
	with cd('/data/vars_project/vars_service/interface/'):
		run('sh stop.sh')
