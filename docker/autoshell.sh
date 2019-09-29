#Запускать в папке с SMS_docker
mv docker SMS_docker
cd ./SMS_docker/redis/redis_data/
rm *
cd
cp appendonly.aof ./SMS_docker/redis/redis_data/
cd ./SMS_docker/redis/ && chown -R 1001:1001 redis_data/
cd redis_data && sudo chown -R 1001:1001 appendonly.aof
cd ../../
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a -f
docker-compose up -d 
