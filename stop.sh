echo "stop port 8001"
lsof -i:8001 | sed '1d' | awk '{print $2}' | xargs kill -9 
echo "clinet stop service on port 8001"
