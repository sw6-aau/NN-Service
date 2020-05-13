#!/bin/bash
echo -e "\e[38;5;172m-===CLEANING===-\e[0m"
docker stop nnservice
docker rm nnservice
echo -e "\n\e[38;5;4m-===BUILDING===-\e[0m\n"
docker build -t service .
echo -e "\n\e[38;5;5m-===RUNNING===-\n\e[38;5;8m(This should just print an ID, otherwise something went wrong..)\e[0m\n"
docker run -d --name nnservice -p 5000:5000 service
echo -e "\n\e[38;5;116m-===CHECK IF SERVICE IS RUNNING===-\e[0m\n"
docker ps
echo -e "\n\e[38;5;202m-===IP OF SERVICE===-\n\e[0m"
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nnservice
echo -e "\n\e[38;5;2m-===DONE===-\e[0m"
