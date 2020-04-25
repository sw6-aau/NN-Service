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
echo -e "\e[38;5;8m(Is expecting a file, via the form, so please test via aSTEP website)\e[0m\n"
#curl -X POST http://localhost:5000/render

echo -e "\n\e[38;5;4m-===TEST '/data'===-\n\e[0m"
curl -X POST http://localhost:5000/data

echo -e "\n\e[38;5;4m-===TEST '/storage/add'===-\n\e[0m"
curl -X POST -F "fileData=@../public/storage/mock.csv" -H 'enctype:multipart/form-data ; Content-Type:multipart/form-data' "http://localhost:5000/storage/add?fileName=hello.txt"

echo -e "\n\e[38;5;4m-===TEST '/storage/get' (the created file)===-\n\e[0m"
curl -X GET "http://localhost:5000/storage/get?fileName=hello.txt"

echo -e "\n\e[38;5;4m-===TEST '/storage/get' (with mock.csv)===-\n\e[0m"
curl -X GET "http://localhost:5000/storage/get?fileName=mock.csv"

echo -e "\n\e[38;5;160m-===TEST '/storage/get' (get service.py attempt)===-\n\e[38;5;8m(This should return 404, otherwise it's possible to get root data...)\e[0m\n"
curl -X GET "http://localhost:5000/storage/get?fileName=../../service.py"

echo -e "\n\e[38;5;4m-===TEST '/storage/get-all-names'===-\n\e[0m"
curl -X GET http://localhost:5000/storage/get-all-names

echo -e "\n\e[38;5;4m-===TEST '/combined'===-\n\e[0m"
curl -X POST http://localhost:5000/combined

echo -e "\n\e[38;5;2m-===DONE===-\e[0m"