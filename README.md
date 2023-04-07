# The aplication for the dentist facility
> The application allows you to manage visits to the company's dental offices. It serves many offices, employees and clients.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## General Information
The application is intended to facilitate the keeping of records for dental offices. It is intended for use by dental staff, not by customers.
The system provides for three roles of registered users: admin, doctor, receptionist.
I created the application as a final project in the online course 'Python from Scratch' organized by the Software Development Academy.


## Technologies Used
- Python - version 3.10.6
- Django - version 4.1.7
- Bootstrap - version 5.3
- DB - sqlite3


## Features
- add, edit and delete employees - admin only
- add clients - authenticated user
- add, edit and delete visits - authenticated user, the system verifies whether the doctor is available at a given time
- add, edit and delete branch offices - admin only
- assign an employee to the office - admin only, an employee can be assigned to multiple offices and can also be "detached" from the office, all appointments for the selected employee in the selected office are deleted
- check the details of the branch office - authenticated user
- check the details of the visit - authenticated user
- a calendar view - authenticated user, the calendar shows free and busy times/dates? for all doctors, an employee can filter by doctors and branch offices
- change the password - authenticated user


## Setup
To run the app you have to: 
- in the terminal go to the project directory ('/project_dentist/'),
- create your virtual environment (e.g. 'python -m venv venv'),
- activate your virtual environment (Windows: 'venv\Scripts\activate', Linux/Mac OS: 'source venv/bin/activate'),
- install Django (e.g. 'pip install Django'),
- go to the project directory where the 'manage.py' file is ('/project_dentist/project_dentist/'),
- run temporary server ('py manage.py runserver'),
- copy the server address to your browser.


## Project Status
Project is: _in progress_.


## Room for Improvement
Room for improvement:
- filter by date of visit
- filter by doctor and client name
- price list

To do:
- when arranging a new visit, it should not be possible to choose an office where a doctor does not work
- recover a forgotten password
- edit and delete clients


## Acknowledgements
The project was created together with:
- Valeriya Kolesnyk,
- Jaroslaw Rogala,
- Grzegorz Sitko,
- Dawid Olejnik.
The calendar is based on FullCalendar by [@Adam Shaw](https://arshaw.com/). Trial version.


## Contact
Created by [@Aleksandra Baszkiewicz](https://www.linkedin.com/in/abaszkiewicz/) - feel free to contact me!
