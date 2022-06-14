# project-awards

## Description
This is a django application the allows users to post their projects that they did and have them reviewed by other perople from a scale of one to ten. They are rated based on design usability and content of their project.


## User Stories
- user can register or sign up to the application
- view posted projects and their details.
- rate other user's projects.
- user can serach for projects.
- view their posted projects.
- view overall score of projects


## Live site
(https://pawards.herokuapp.com/)


## Technologies used
* Django Framework - used to create the application. 
* Heroku - used to deploy the application. 

## Set up and installation
#### Clone the Repo
####  Activate virtual environment
Activate virtual environment using python as default handler
    `virtualenv -p /usr/bin/python venv && source venv/bin/activate`
For windows users use this to activa your environment
   ` source venv/Scripts/active`    
####  Install dependancies
Install dependancies that will create an environment for the app to run `pip3install -r requirements.txt`
####  Create the Database
    - psql
    - CREATE DATABASE <DBNAME>;
####  .env file
Create .env file and add the following filling where appropriate:

    SECRET_KEY = '<Secret_key>'
    DBNAME = '<DBNAME>'
    USER = '<Username>'
    PASSWORD = '<password>'
    DEBUG = True
#### Run initial Migration
    python3.6 manage.py makemigrations gallery
    python3.6 manage.py migrate
#### Run the app
    python3.6 manage.py runserver
    Open terminal on localhost:8000

## Known Bugs

## Contact Information
If you have any questions feel free to contact me.

## License
* MIT LICENSE
* Copyright (c) 2022 Joyce Njoroge