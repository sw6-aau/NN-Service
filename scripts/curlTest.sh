#!/bin/bash
echo -e "-===TEST'/'===-\n"
curl http://localhost:5000
echo -e "\n-===TEST '/info'===-\n"
curl http://localhost:5000/info
echo -e "\n-===TEST '/fields'===-\n"
curl http://localhost:5000/fields
echo -e "\n-===TEST '/readme'===-\n"
curl http://localhost:5000/readme
echo -e "\n-===TEST '/render'===-\n"
curl -X POST http://localhost:5000/render
echo -e "\n-===TEST '/data'===-\n"
curl -X POST http://localhost:5000/data
echo -e "\n-===TEST '/combined'===-\n"
curl -X POST http://localhost:5000/combined
echo -e "\n-===DONE===-"