#! /bin/bash

#remove all containers - by wonseok (2017/01/15)
 docker rm -f $(docker ps -a -q)
 for f in `docker images | grep -v IMAGE | awk '{split($0,array," ")} {print array[3]}'`
 do
  echo "==> delete image : $f"
  docker rmi $f
done

# create necessary images
docker build --tag node-nginx:app .
cd nginx
docker build --tag node-nginx-lb:app .
cd ../

# run docker-compose up
docker-compose up -d
