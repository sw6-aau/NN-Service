#!/bin/bash
echo -e "-===CLEAN ALL DOCKER===-\nPlease make sure you want to clean everything (do you use Docker for other things?)\n"
docker system prune -a
echo -e "\n-===DONE===-"