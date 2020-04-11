#!/bin/bash
echo -e "\e[38;5;4m-===GET IP OF DOCKER SERVICE===-\n\e[0mPlease enter service:"
read service
echo -e "\n\e[38;5;202m-===IP OF SERVICE===-\n\e[0m"
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $service
echo -e "\n\e[38;5;2m-===DONE===-\e[0m"