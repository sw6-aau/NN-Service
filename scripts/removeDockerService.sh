#!/bin/bash
echo -e "-===REMOVE DOCKER SERVICE===-\nPlease enter service:"
read service
echo -e "\n-===STOPPING SERVICE===-\n(This should just print an ID, otherwise something went wrong..)\n"
docker stop $service
echo -e "\n-===REMOVING SERVICE===-\n(This should just print an ID, otherwise something went wrong..)\n"
docker rm $service
echo -e "\n-===RUNNING SERVICES===-\n"
docker ps
echo -e "\n-===DONE===-"