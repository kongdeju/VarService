echo "start api service"
nohup gunicorn -w 4 -k gevent -b  0.0.0.0:8000  Api:app 1>>run.log 2>>run.log &
echo "run in backgroud on port 8000"
