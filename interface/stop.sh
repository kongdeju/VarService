echo "Stopping api service"
lsof -i:8000 | sed '1d' |  awk '{print $2}' | xargs kill -9 
echo "api service is stopped"
