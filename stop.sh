lsof -i:8001 | awk '{print $2}' | xargs kill -9 
