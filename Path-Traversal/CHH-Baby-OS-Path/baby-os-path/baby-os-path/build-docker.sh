#!/bin/bash
docker rm -f babyospath
docker build --tag=babyospath .
docker run -p 1337:1337 --rm --name=babyospath babyospath