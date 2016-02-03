echo "client is running "
nohup gunicorn -w 4 -k gevent -b  0.0.0.0:8001  VarsService:app 1>>/dev/null 2>>/dev/null &
echo "port 8001 is listening"
