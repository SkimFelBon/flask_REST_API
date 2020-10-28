# Flask_REST_API for Social Network

### Getting Started
## Installation:
```sh
sudo pip install virtualenv
git clone https://github.com/SkimFelBon/flask_REST_API
cd ./flask_REST_API/
# activate virtualenv
virtualenv env
sudo pip install -r requirements.txt
# pull postgres-image from docker hub: https://hub.docker.com/_/postgres
docker pull postgres
# start docker container
docker run --name my_psql -p 127.0.0.1:3306:3306 -e POSTGRES_PASSWORD=admin -d postgres:latest
# connect to container
docker exec -it my_psql bash
```
### Create database
```sh
# connect to postgresql from command line:
psql -U postgres
```
```sql
CREATE DATABASE rest_api;
-- verify that db was created (list all databases with \l command):
\l
```
### from host copy dumpfile to container
```sh
docker cp ./dumpfile my_psql:/root/dumpfile
# jump to container and dump data to database:
psql rest_api < dumpfile -U postgres
```
### jump to psql one more time, select db and verify that data exists:
```sql
psql -U postgres
-- connect to our database:
\c rest_api
-- verify data:
select * from "user";
```
## also create settings.py
```py
# settings.py
DB_NAME = "rest_api"
USER = "postgres"
PASS = "yourpassword"
SECRET_KEY = 'replace-me'
SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASS}@localhost/{DB_NAME}?client_encoding=utf8"
```
## start app
```sh
flask run
```
#### Basic features:
* [x] `POST /api/signup` user signup.
* [x] `POST /api/login` user login.
* [x] `POST /api/post` post creation.
* [x] `PUT /api/like/<int:post_id>` post like.
* [x] `PUT /api/unlike/<int:post_id>` post unlike.
* [x] `GET /api/analytics/?date_from=2020-02-02&date_to=2020-02-15` analytics about how many likes was made. Analytics aggregated by day
* [x] `GET /api/users/<int:prim_key>` search user.
* [x] user activity an endpoint which will show when user was login last time and when he mades a last request to the service.
* [x] Implemented token authentication, using JWT
#### Signup route
```sh
http://127.0.0.1:5000/api/signup/
```
```json
{"first_name":"Edward",
  "last_name":"LaFontainer",
  "password":"12345",
  "email":"Edward.LaFontainer@mail.com"}
```
response:
```json
{
  "message": "Created new User.",
  "user": {
    "email": "Edward.LaFontainer@mail.com",
    "first_name": "Edward",
    "id": 4,
    "last_login": null,
    "last_name": "LaFontainer",
    "last_request": null
  }
}
```
#### Login route
```sh
http://127.0.0.1:5000/api/login/
```
```json
{"email":"Edward.LaFontainer@mail.com","password":"12345"}
```
response:
```json
{
  "token": "eyJhbG...aHO4-subrC0"
}
```
#### Post creation route
```sh
http://127.0.0.1:5000/api/post
```
```json
{"title":"my post", "description":"lorem ipsum dolor sit amet..."}
```
response:
```json
{
  "message": "Created new post.",
  "post": {
    "author_id": 4,
    "created": "2020-07-19T15:24:49.510789",
    "description": "description",
    "id": 2,
    "title": "title"
  }
}
```

#### Like route
```sh
http://127.0.0.1:5000/api/like/1
```
response:
```json
{
  "message": "Liked post"
}
```
#### Unlike route
```sh
http://127.0.0.1:5000/api/unlike/1
```
response:
```json
{
  "message": "Unliked post"
}
```
#### analytics
```sh
http://127.0.0.1:5000/api/analitics/?date_from=2020-07-17&date_to=2020-07-20
```
response:
```json
{
  "likes_per_day": [
    [
      18.0,
      1
    ],
    [
      19.0,
      2
    ]
  ]
}
```
#### search user route
```sh
http://127.0.0.1:5000/api/users/1
```
response:
```json
{
  "user": {
    "email": "Amy.Meyer@mail.com",
    "first_name": "Amy",
    "id": 1,
    "last_login": "2020-07-19T11:52:23.884529",
    "last_name": "Meyer",
    "last_request": "2020-07-19T11:52:33.849130"
  }
}
```
