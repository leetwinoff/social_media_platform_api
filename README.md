# Social Media Platform API

## Description

### Features
#### User Profiles
- Users can create their profiles and provide information such as profile picture and bio.
- Each user has a unique profile associated with their account.

#### Posts

- Users can create posts by uploading images and adding a description.
- Posts can be tagged with relevant keywords to categorize content.
- Users can view a feed of posts from other users.

#### Likes and Comments
- Users can like posts to show their appreciation for the content.
- Users can leave comments on posts to share their thoughts.

#### Follow and Unfollow
- Users can follow other users to stay updated with their posts.
- Users can unfollow other users to stop receiving updates from them.

## Installation

```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt 
```

```python
# Rename the .env.sample file to .env.
# Inside the .env file, set the SECRET_KEY variable to a secure secret key for your Django application.

# Make all migrations and run server

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```



