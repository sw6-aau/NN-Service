#!/bin/bash
echo -e "\e[38;5;124m-===REMOVE DOCKER SERVICE===-\n\e[0mPlease enter service:"
read service
echo -e "\n\e[38;5;110m-===STOPPING SERVICE===-\n\e[38;5;8m(This should just print an ID, otherwise something went wrong..)\e[0m\n"
docker stop $service
echo -e "\n\e[38;5;202m-===REMOVING SERVICE===-\n\e[38;5;8m(This should just print an ID, otherwise something went wrong..)\e[0m\n"
docker rm $service
echo -e "\n\e[38;5;4m-===RUNNING SERVICES===-\n\e[0m"
docker ps
echo -e "\n\e[38;5;2m-===DONE===-\e[0m"