
# YourSkoolYorWay Back end API

## Installation
### Step - 1
#### Clone the project
``` git clone https://github.com/Your-Skool-Your-Way/ysywbackend-API.git```
### Step - 2
#### Create Virtualenvironment
``` virtualenv venv```
### Step - 3
#### Activate virtualenv
``` source venv/bin/activate```
### Step - 4
#### Install all depedancies
``` pip install -r requiements.txt``` or ``` make install```
### Step - 5
#### Initial set up
``` make set-up``` or
```python manage.py createrole --settings=YourSkoolYoueWayP1.settings.development``` and 
```python manage.py createsuperadmin settings=YourSkoolYoueWayP1.settings.development```

### Step - 6
#### runserver
``` make runserver``` or
```python manage.py runserver --settings=YourSkoolYoueWayP1.settings.development```
### Step - 7
#### API documentaion URL
- Swagger :- http:1270.0.1:8000/swagger/
- Redoc :- http:1270.0.1:8000/redoc/
