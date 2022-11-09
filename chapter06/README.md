# 데이터베이스 실습

## 1. 도커로 MySQL 설치

>도커로 MySQL을 설치하고 실습함.

### MySQL 이미지 받기

```shell
docker pull mysql
```

### MySQL 컨테이너 실행하기

- YOUR_DB_PASSWORD : DB 로그인과 연결에 사용할 패스워드 입력하기

- MySQL 도커 컨테이너 생성
```shell
docker create \                       
--name mysql_container \
-e MYSQL_ROOT_PASSWORD="{YOUR_DB_PASSWORD}" \
-p 3306:3306 \
mysql:latest
```

- MySQL 도커 컨테이너 실행
```shell
docker container start mysql_container 
```

### MySQL 컨테이너 접속

```shell
docker exec -it mysql_container bash
```

- 비밀번호는 앞서 컨테이너 생성할 때 입력했던 YOUR_DB_PASSWORD을 동일하게 입력


## 2. 데이터베이서 설정 및 테이블 생성

- 6장 API에 데이터베이스 연결하기 참조

## 3. SQLAlchemy에서 데이터베이스 연결

- `ex_db_connect.py` 참조


## Reference

- [Docker를 이용하여 MySQL 설치하고 접속하기](https://happymemoryies.tistory.com/68)