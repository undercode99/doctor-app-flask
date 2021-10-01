# Restful API Doctor app with Flask

Simple restfull api app doctor appointments, build with python flask this app already scabelable with the versioning api, and separate layers.

Features:
- Docker environment with compose integrate gunicorn, postgres
- Auth with JWT
- Flask scheduler for update data google big query
- Unit Testing with pytest
- ORM with sqlalchemy
- Migration with alembics
- Validator api http with cerberus 



## Information API

- **Documentation API Postman** :
   
   https://documenter.getpostman.com/view/17611308/UUy38m3U 



# Getting start
1. Clone this repository

   ```$ git clone https://github.com/undercode99/doctor-app-flask.git ```

   Enter directory

   ```$ cd doctor-app-flask ```

3. Create file .env and add config database and sekeret key

    Example: 
    ```env
    FLASK_ENV=prod
    FLASK_APP=serve:app
    DEBUG=False
    SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user_pg:password_pg123@pg:5432/db_pg
    SECRET_KEY=da8dhajs7dhqe23r3i18rh32nmr2yr23mhmr2o3r9o23hjrfwefjnsmf8wefksdf
    GOOGLE_CLOUD_CREDENTIAL=google-cloud-credentials.json

    POSTGRES_USER=user_pg
    POSTGRES_PASSWORD=password_pg123
    POSTGRES_DB=db_pg
    ```

4. Build & Deploy
   
   - Build

   ```$ docker-compose build ```

   - Deploy and Running In Background

   ```$ docker-compose up -d```
   
5. Running already running with port 80
   
   http://localhost/api/v1/login
 
   Auth login employee default:

    username : **employee**
    
    password : **employee123**
