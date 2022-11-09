#!/bin/bash
API_URL="http://localhost:9292"

# hello world
http -v GET "$API_URL"

# ping
http -v GET "$API_URL/ping"

# sign up : 회원가입
http -v POST "$API_URL/sign_up" username="park" email="park@helloworld.org"
http -v POST "$API_URL/sign_up" username="kang" email="kang@helloworld.org"
http -v POST "$API_URL/sign_up" username="yoon" email="yoon@helloworld.org"
http -v POST "$API_URL/sign_up" username="choi" email="choi@helloworld.org"
http -v POST "$API_URL/sign_up" username="shim" email="shim@helloworld.org"


# follow : 팔로우
http -v POST "$API_URL/follow" user_id_follow_origin=1 user_id_follow_target=3
http -v POST "$API_URL/follow" user_id_follow_origin=1 user_id_follow_target=4
http -v POST "$API_URL/follow" user_id_follow_origin=2 user_id_follow_target=1
http -v POST "$API_URL/follow" user_id_follow_origin=3 user_id_follow_target=1
http -v POST "$API_URL/follow" user_id_follow_origin=3 user_id_follow_target=5
http -v POST "$API_URL/follow" user_id_follow_origin=4 user_id_follow_target=1
http -v POST "$API_URL/follow" user_id_follow_origin=4 user_id_follow_target=2
http -v POST "$API_URL/follow" user_id_follow_origin=4 user_id_follow_target=3
http -v POST "$API_URL/follow" user_id_follow_origin=5 user_id_follow_target=1
http -v POST "$API_URL/follow" user_id_follow_origin=5 user_id_follow_target=3
http -v POST "$API_URL/follow" user_id_follow_origin=5 user_id_follow_target=4


# tweet : 트윗 작성
http -v POST "$API_URL/tweet" user_id=1 tweet="This is written by 1, Hello World"
http -v POST "$API_URL/tweet" user_id=1 tweet="This is written by 1, I hate this world"

http -v POST "$API_URL/tweet" user_id=2 tweet="This is written by 2, Hello World"
http -v POST "$API_URL/tweet" user_id=2 tweet="This is written by 2, I hate this world"

http -v POST "$API_URL/tweet" user_id=3 tweet="This is written by 3, Hello World"
http -v POST "$API_URL/tweet" user_id=3 tweet="This is written by 3, I hate this world"

http -v POST "$API_URL/tweet" user_id=4 tweet="This is written by 4, Hello World"
http -v POST "$API_URL/tweet" user_id=4 tweet="This is written by 4, I hate this world"

http -v POST "$API_URL/tweet" user_id=5 tweet="This is written by 5, Hello World"
http -v POST "$API_URL/tweet" user_id=5 tweet="This is written by 5, I hate this world"

http -v POST "$API_URL/tweet" user_id=1 tweet="This is written by 1, this service ... ?"
http -v POST "$API_URL/tweet" user_id=1 tweet="This is written by 1, oh WOW"

http -v POST "$API_URL/tweet" user_id=4 tweet="This is written by 4, life is fun"
http -v POST "$API_URL/tweet" user_id=4 tweet="This is written by 4, let's enjoy them"

http -v POST "$API_URL/tweet" user_id=5 tweet="This is written by 5, life is dumb"
http -v POST "$API_URL/tweet" user_id=5 tweet="This is written by 5, forget about it"