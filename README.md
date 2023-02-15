# CeladonApi
<sub>A C18 Ada Developers Academy web backend capstone completed in 3 weeks</sub>

Celadon is a gamified task management web app for busy students and lifelong learners where users can cleanly organize multiple task lists by context categories and level Pokemon for each task completed.

<sub>[Sibling repository can be found here](https://github.com/yaelso/celadon-client)</sub>

![Latest Release](https://img.shields.io/github/v/release/yaelso/CeladonApi)  ![Deployment State](https://img.shields.io/github/deployments/yaelso/CeladonApi/celadon-api)  ![License](https://img.shields.io/github/license/yaelso/CeladonApi)

## Learning Goals
- Demonstrate self direction, time management, and independent learning
- Learn and implement new technologies for both development and deployment
- Complete a product life cycle from conception to delivery, including deployment
- Utilize agile practices to assist project completion
- Implement complex relationships between components and cleanly manage multiple moving parts on both the front and back end
- Explore user authentication and data persistence

## Features
Users can login via Google and access a number of views, varying from a dashboard that contains all productivity models belonging to a user, an archive, a Pokedex, and a personal profile.

- User login and auth via Google
- Category, list, and task creation
- Archived and favorite checklists, task scheduling, and task progress/completion status markers
- Incrementable habits
- Pokemon collection, EXP gathering, and leveling

## Usage Notes
This server repository lacks Firebase configuration keys! To run locally, you can hook up your own Firebase auth configuration values to the appropriate keys contained in `app/__init__.py`. 

Unit tests are not currently functional for need of mock JWTs!

## Installation
This project does not have any current distribution packages! Below are steps describing how to run CeladonApi locally...

1. Clone repository
2. Create a virtual env
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ # You're in activated virtual environment!
```
3. Install dependencies
```
(venv) $ pip install -r requirements.txt
```
4. Create database and corresponding env vars to link project to Postgresql DB, resembling the following:
```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/celadon_api_development
```
5. Run `$ flask db init` and apply migrations
6. Plug in personal Firebase auth configuration values
7. Run server via `flask run`

### Dependencies
```
Flask-Cors==3.0.10
Flask-SQLAlchemy==2.4.4
flask-firebase-admin==0.2.4
gunicorn==20.1.0
psycopg2-binary==2.9.5
requests==2.25.1
SQLAlchemy==1.3.23
```
