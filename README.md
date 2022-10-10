# Dockerized URL Shortener API

API link shortening service written on DRF

## Installing using Github

Install PostgreSQL and create db

```shell
git clone https://github.com/denlubn/url-shortener.git
python3 -m venv venv
source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
python manage.py migrate
python manage.py runserver
```
### Run with docker

Docker should be installed

```shell
docker-compose build
docker-compose up
```

Getting access
-
- create user via /user/register/
- get access token via /user/token/


Features
-
- JWT authenticated
- Admin panel /admin/
- Documentation is located at /doc/swagger/
- Managing urls
- Creating and customize short url
- Every url has counter
- Pagination
- Registration by mail instead of username
