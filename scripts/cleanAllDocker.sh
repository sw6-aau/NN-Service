#!/bin/bash
echo -e "\e[38;5;124m-===CLEAN ALL DOCKER===-\nPlease make sure you want to clean everything (do you use Docker for other things?)\e[0m\n"
docker system prune -a
echo -e "\n\e[38;5;2m-===DONE===-\e[0m"