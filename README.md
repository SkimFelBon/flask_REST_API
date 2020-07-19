# Flask_REST_API

### Installation:
## Getting Started
```
sudo pip install virtualenv
git clone https://github.com/SkimFelBon/flask_REST_API
cd ./flask_REST_API/
sudo pip install -r requirements.txt
```
#### list of routes:
* user signup. POST
* user login. POST
* post creation. POST
* post like. PUT
* post unlike. PUT
* analytics about how many likes was made. Example url
/api/analytics/?date_from=2020-02-02&date_to=2020-02-15. analytics aggregated by day. GET
* search user. GET
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
