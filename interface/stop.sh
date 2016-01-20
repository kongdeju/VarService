lsof -i:8000 | awk '{print $2}' | xargs kill -9 
