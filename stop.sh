lsof -i:7000 | awk '{print $2}' | xargs kill -9 
