#!/bin/bash
echo -e "-===BUILDING===-\n"
docker build -t service .
echo -e "\n-===RUNNING===-\n(This should just print an ID, otherwise something went wrong..)\n"
docker run -d --name nnservice -p 5000:5000 service
echo -e "\n-===CHECK IF SERVICE IS RUNNING===-\n"
docker ps
echo -e "\n-===DONE===-"