# S3_AJAX_API

## Sample endpoint usage

### Students

#### Get all students

```bash
curl http://127.0.0.1:5000/students
```

#### Create a student with interests

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"Gift Chimphonda", "interests":["1", "2"]}' http://127.0.0.1:5000/students
```

### Interests

#### Get interests

```bash
curl http://127.0.0.1:5000/interests
```

#### Get interest with specified id

```bash
curl http://127.0.0.1:5000/interests/1
```

#### Create an interest

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"Scrabble"}' http://127.0.0.1:5000/interests
```

#### Edit an interest with specified id

```bash
curl -X PATCH -H 'Content-Type:application/json' -d '{"name":"Bawo"}' http://127.0.0.1:5000/interests/2
```

```bash
curl -X DELETE http://127.0.0.1:5000/interests/3
```

## Prerequisites

- Python 3
- PostgreSQL
- Internet browser
  
## How to set  and run the project

- Virtual environment setup
  - create a virtual environment `python -m venv env`
  - Activate the virtual environment
    - for windows `env\Scripts\activate`
    - for linux\macOS `source env/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Set env variables
  - Change the values in env.sh (Linux / macOs) or env.bat (Windows)
  - Run the env script on the terminal `env.bat` or `env.sh`
- Apply migrations to database `flask db upgrade`
- Run the project
  - `python -m app.py` or `flask run`
