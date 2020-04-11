#!/bin/bash
echo -e "\e[38;5;4m-===TEST'/'===-\n\e[0m"
curl http://localhost:5000
echo -e "\n\e[38;5;4m-===TEST '/info'===-\n\e[0m"
curl http://localhost:5000/info
echo -e "\n\e[38;5;4m-===TEST '/fields'===-\n\e[0m"
curl http://localhost:5000/fields
echo -e "\n\e[38;5;4m-===TEST '/readme'===-\n\e[0m"
curl http://localhost:5000/readme
echo -e "\n\e[38;5;4m-===TEST '/render'===-\n\e[0m"
curl -X POST http://localhost:5000/render
echo -e "\n\e[38;5;4m-===TEST POST '/data'===-\n\e[0m"
curl -X POST http://localhost:5000/data
echo -e "\n\e[38;5;4m-===TEST POST '/storage'===-\n\e[0m"
curl -X POST http://localhost:5000/storage
echo -e "\n\e[38;5;4m-===TEST GET '/storage'===-\n\e[0m"
curl -X GET http://localhost:5000/storage
echo -e "\n\e[38;5;4m-===TEST '/combined'===-\n\e[0m"
curl -X POST http://localhost:5000/combined
echo -e "\n\e[38;5;2m-===DONE===-\e[0m"