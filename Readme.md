## Social Application Backend

Made with

- Django
- Django Rest Framework

Authentication using JWT Tokens

Provide various functionalities

- Create User
- Validate email id
- Create Post
- Retrieve Post
- Update, Delete Post
- Follow, Unfollow Users
- Retrieve List of who follow you and who you follow
- Like Post, Unlike Post, Comment on Post
- Search Users
- Update User Profile Photo

### Run the project

```shell
$ python manage.py makemigrations
```

```shell
$ python manage.py migrate
```

```shell
$ python manage.py runserver
```

Celery is required to send user email for account verification Start redis on port 6379 and start celery using following
command

```shell
$ celery -A social_application worker --loglevel=info
```

Link to frontend [repository](https://github.com/spiderxm/friend-book)

Made By [Mrigank Anand](https://github.com/spiderxm)