# poll-test-django-app
This is a Django app developed as one of the required job interview steps (team lead)

I was given a time constraint of 3-4 hours.
Somehow I didn't manage to fit in this timeframe.
It took me about 20 hours to make this minimal version. (+-3 hours a day for 5 days + xtra for some thoughts).
While I was working on the app new product insights were constantly coming up and I had to stop and think over.
However I didn't have to make any significant changes while working on the app (thanks separation of responsibility).

Here are the main requirements >>>

# User types

## Admins
- Can authorize (no registration)
- Quiz CRUD operations

## Client
- Get list of active polls
- Pass quiz (anonymously?)
- Get list of previously passed polls

# Data attributes

## Poll
- name
- start date (cannot be changed after creation)
- end date

## Poll question
- question text
- type (TEXT, Single choice, Multiple choice)

Should be implemented using Djnago (2.2.10) and DRF.

# Implementation

Since I really needed to use JSONFields I didn't stick with the Django 2x and switched to the latest version. I believe that sticking to 2x is generally silly.
This is unless you have some legacy stuff that basically forces you to use an older version of the framework.

There are 3 apps within the Django project

## Common
Holds the custom user model.

## Poll
Represents what is called a poll template. It is created by the admin.

## Client poll
Is created using the template when Client wants to pass the poll. 
Basically a data transfer object. 
Need this because the template might be altered during active poll test by user.

## Client poll answer
Holds json data that client provided when submitting the poll. 
Assuming the client app is spa or mobile we only get the whole package of answers. Not one by one.
When saving the answer we also save some xtra data from the questions.

# Quickstart

1) Create python environment and activate it
2) pip install -r requirements.txt
3) pip manage.py test

Check the tests and urls.
The views are pretty basic with few customizations.

# API Endpoints

## Admin
- /polltemplate/list/
- /polltemplate/<ID>/update/
- /polltemplate/<ID>/update/ordering/
- /polltemplate/<ID>/delete/
- /polltemplate/create/
- /polltemplate/<ID>/question/<ID>/update/
- /polltemplate/<ID>/question/<ID>/delete/
- /polltemplate/<ID>/question/add/
- /api-token-auth/

## Client
- /polltemplate/
- /poll/create/
- /poll/submit
- /poll/list

Naviagte endpoints in browser to get more insights or ask dev.
Can get more info while wiewing the urls, views, serializers and tests.
