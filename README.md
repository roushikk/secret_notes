# Secret Notes

This project is a clone of  [privnote](https://privnote.com/).
 I did not like how a few things work with privnote so I decided to make my own version of it

 Here's how this website is different than privnote:

-   You can set the title of the note
-   You can set how many reads are allowed
-   You can set any time of expiry
-   You can set the amount of reads as well as expiry time on the same note
-   Note is not destroyed if the person enters a wrong password

# Demo
## [https://secret.roushik.com](https://secret.roushik.com)


# Deploy Development
Deploy the docker-compose.yml file

    docker-compose -f docker-compose.yml up -d
Run Migrations

    docker-compose -f docker-compose.yml exec web python manage.py migrate
Access on [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000)

# Deploy Production
Copy .env.dev to .env.prod file and change sensitive information
Information to Change:

 - Change `DJANGO_DEBUG` to `0`
 - Change `DJANGO_SECRET_KEY` using [https://djecrety.ir/](https://djecrety.ir/)
 - Change `DB_PASSWORD` and `POSTGRES_PASSWORD` to something secure (both values should be the same)

Deploy the docker-compose.yml and docker-compose.prod.yml file

    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

Run Migrations and Collect Static Files

    docker container exec -it secret_notes_web_1 bash
Inside docker container, run

    python manage.py migrate
    python manage.py collectstatic

Note

> Django does not server static files in production, you need to serve the staticfiles/ folder at /static/ using nginx or any other web server

