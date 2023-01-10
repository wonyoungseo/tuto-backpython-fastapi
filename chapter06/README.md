# 챕터 6: 데이터베이스

>데이터베이스 연결하기

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

```text
mysql -u root -p
```

- 비밀번호는 앞서 컨테이너 생성할 때 입력했던 YOUR_DB_PASSWORD을 동일하게 입력


## 2. 데이터베이서 설정 및 테이블 생성

- 6장 API에 데이터베이스 연결하기 참조

### 2.1. 쿼리

```mysql
CREATE DATABASE miniter;
USE miniter;

CREATE TABLE users(
 id INT NOT NULL AUTO_INCREMENT,
 name VARCHAR(255) NOT NULL,
 email VARCHAR(255) NOT NULL,
 hashed_password VARCHAR(255) NOT NULL,
 profile VARCHAR(2000) NOT NULL,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 UNIQUE KEY email (email)
);

CREATE TABLE users_follow_list(
    user_id INT NOT NULL,
    follow_user_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, follow_user_id),
    CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES users(id),
    CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
);

CREATE TABLE tweets(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    tweet VARCHAR(300) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES
    users(id)
);

SHOW tables;
EXPLAIN users;
EXPLAIN users_follow_list;
EXPLAIN tweets;
```

## 3. SQLAlchemy에서 데이터베이스 연결해보기

- `ex_db_connect.py` 참조

## 4. SQLAlchemy를 적용한 구현

- 베이직
  - `chp06_app_01_basic.py`
- 응용
  - `chp06_app_02_applied.py` (TBU) 

## 4. 엔드포인트 실행

### 4.1. 회원가입 엔드포인트

```bash
http -v POST "http://localhost:9292/sign_up" name="kim" email="kim@helloworld.org" password="test1234" profile="test_kim"
```

### 4.2. 트윗 엔드포인트

```bash
http -v POST "http://localhost:9292/tweet" id=1 tweet="Hello World"
```

### 4.3. 트윗 엔드포인트

```bash
http -v GET "http://localhost:9292/timeline/?user_id=1"
```


### 4.4 팔로우 언팔로우 엔드포인트

```bash
http -v POST "http://localhost:9292/follow" user_id_origin=2 user_id_target=2
```

```shell
http -v POST "http://localhost:9292/unfollow" user_id_origin=2 user_id_target=2
```



## Reference

- [Docker를 이용하여 MySQL 설치하고 접속하기](https://happymemoryies.tistory.com/68)