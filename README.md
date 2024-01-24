# FishCard Platform
Web app for fishcards

## Project setup
### Setup virtual env and pip.
Windows
```
> python -m venv env
```
Linux
```
$ virtualenv env
```
### Activate virtual env
Linux
```
$ source env/bin/activate
```
Windows
```
> env\scripts\activate
```
### Download packages
```
$ pip install -r requirements.txt
```
### .env
Create .env file or rename .env.local to .env

### Change directory
```
cd fishcards
```
### Do migration
```
$ python manage.py migrate
```
### Create superuser
```
$ python manage.py createsuperuser
```
### Optional: load data
```
$ python load_data.py
```
### Run server
#### on ip:
```
$ python manage.py runserver 0.0.0.0:8000
```
#### locally:
```
$ python manage.py runserver
```
## Available sets

- IoT - 166 cards - Author: [Jakub-Ner](https://github.com/Jakub-Ner)

- .Net - 42 cards - Author: [DBorner](https://github.com/DBorner)

## Screenshots

![Screenshot1](__screenshots/1.png?raw=true "Title")
![Screenshot2](__screenshots/2.png?raw=true "Title")
![Screenshot3](__screenshots/3.png?raw=true "Title")
![Screenshot4](__screenshots/4.png?raw=true "Title")
![Screenshot5](__screenshots/5.png?raw=true "Title")
![Screenshot6](__screenshots/6.png?raw=true "Title")
![Screenshot7](__screenshots/7.png?raw=true "Title")