#!/bin/bash
echo -e "-===GET IP OF DOCKER SERVICE===-\nPlease enter service:"
read service
echo -e "\n-===IP OF SERVICE===-\n"
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $service
echo -e "\n-===DONE===-"