# **\*\*\*\***\*\*\***\*\*\*\***

# About this project: 

- what is does? It handles user authentication, validation, and creation. And for every account made, creates a lead in a Monday.com board. It can eaisly plug into any front end form you make by passing simply {first_name: "", last_name: "", email: ""} at a minimum. I also set up some demo apps and a celery beat scheduler. Very customizable. 


- I made this repository public because it doesnt contain sensitive information, and is a good baseline for bnuisiness level software.
- If you want to use it feel free to clone it and build up on it. But here are some things you should know

  1: If you want to start this project you should be familiar with the django-reest-framework and Celery at least
  2: Right now there are some bugs from stripping out all sensitiver information. So dont expect to open this up very easily right now.
  3: I do try and keep this up to date with patches of my own, but if you want to make any changes feel free to submit a pr into the dev branch


# Starting The Project

- First you need to open the projects vertual environment and install the dependencies

  1: Open a terminal navigated to the root of this project
  2: Run the command `pipenv shell && pipenv install`
  3: Before starting the server you should follow the rest of the steps...

# **\*\*\*\***\*\*\***\*\*\*\***

# Set environment variables

- There are some environment variables you need to set up

  1: Create a new file called .env and put it in the boilerplate_django_celery root directory
  2: At the bottom of the read me you will find the environment variables
  3: Just copy and past them in your .env and fill in all the fields as you go

# **\*\*\*\***\*\*\***\*\*\*\***

# Set up a database

- You need a PostgreSQL database to run this project.
- If you don't have one you can download it here -> `https://www.postgresql.org/download/`
- You could also get "PG Admin 4" or some other database GUI to help.

  1: You need to create a database, and a postgres user in the GUI, or in the comand line
  2: And save the details to use in these environment variables:

  - DB_NAME=
  - DB_USER=
  - DB_PASSWORD=

# **\*\*\*\***\*\*\***\*\*\*\***

# Create a super user

- Next you need to create a admin user for yourself

  1: In your normal django terminal, navigated to the root of this app,
  Run the command `pipenv shell && python manage.py createsuperuser`
  2: Follow the text propts in the terminal.
  3: Use something you will remember easily.

# **\*\*\*\***\*\*\***\*\*\*\***

# Start the server

- Start the app

  1: Run the command `pipenv shell && python manage.py runserver`
  2: In your browser go to `http://localhost:8000/admin/`
  3: Login with your super user credentials from the last step.

- Next you just need to set up the front end.

# **\*\*\*\***\*\*\***\*\*\*\***

# CELERY SETUP

1: RabbitMQ Setup

- You need to install rabbitmq on your machine. Set up will be different for different os, it might be kind of a pain.
  - See here for help with rabbitmq => https://docs.celeryq.dev/en/v4.2.1/getting-started/brokers/rabbitmq.html
  - But no matter what you need rabbitmq setup on your machine. https://www.rabbitmq.com/
  - And set `RABBITMQ_USERNAME=` & `RABBITMQ_PASSWORD=` environment variables
  - Thats it! Now just turn it all on!

2: Turn It On

- Open up a terminal on the side somethere, you'll need at least 3.
- In the first terminal, start your rabbitmq server => `sudo rabbitmq-server`
- Open another new server and navigate to the root of this app,
  from there run => `pipenv shell && celery -A boilerplate_django_celery worker -l INFO`
- Repeat the previous step but run this command => `pipenv shell && celery -A boilerplate_django_celery worker -B`

And now your done, and ready to starty using Celery!

# **\*\*\*\***\*\*\***\*\*\*\***

# HOW TO KNOW YOUR PROPERLY SETUP?

- You should have a running frontend and backend...
- You should also have at least 3 other terminals open and running:

  - a rabbitmq server, celery worker, celery beat
  - If you watch the celery-beat terminal for a while you should see "Checking customer packages..." every minute or so

- Next I would just create a bunch of customers using the basit user registration form. You should see lots of print statements.
  - Hopefully you dont see any `Error: ` logs, then somethings gone wrong...

# **\*\*\*\***\*\*\***\*\*\*\***

# EVNIRONMENT VARIABLES

- Copy and paste the rest of the file into your .env and fill out the empty variables.

# Database

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=5432

SECRET_KEY=

# Monday

MONDAY_API_KEY=

