# quiz-test-django-app
This is a Django app developed as one of the required interview steps

I was asked to create a django base rest api for a poll app which should have the following characteristics:

# User types

## Admins
- Can authorize (no registration)
- Quiz CRUD operations

## Client
- Get list of active polls
- Pass quiz (anonymously?)
- Get list of previously passed polls

# Data attributes

## Quiz
- name
- start date (cannot be changed after creation)
- end date

## Quiz question
- question text
- type (TEXT, Single choice, Multiple choice)

Should be implemented using Djnago (2.2.10) and DRF.

# Implementation

Since I really needed to use JSONFields I didn't stick with the Django 2x and switched to the latest version. I believe that sticking to 2x is silly and generally bad practice.
Unless you have some legace stuff that basically forces you to use an older version of the framework.

There are 3 apps within the Django project

## common
Holds the custom user model.

## Poll
Represents what is called a poll template. It is created by the admin.

## Client poll
Is created using the template when Client wants to pass the poll. 
Basically a data transfer object. 
Need this because the template might be altered during active poll test by user.


