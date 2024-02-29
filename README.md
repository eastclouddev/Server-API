# Server-API


## Server-APIの環境を単独で起動する方法
1. Server-APIへ移動する
```
cd Server-API
```

2. Dockerをbuildする
```
docker build -f environment/develop/Dockerfile . -t myapp
```

3. Dockerを起動する
```
docker run -p 8000:8000 myapp
```
