# mock-con-2020-word-cloud
Takes in HTML articles and archives word usage and time information

## Dev Setup ##
Make sure that Docker desktop is installed and running before setup.

1. Install Python Virtualenv and Database Manager
```
pip3 install pipenv alembic --user
```

2. Install Python packages from Pipfile.lock
```
pipenv install 
```

3. Start Database
```
docker-compose up
```

4. Migrate Database
```
pipenv shell
PYTHONPATH=. alembic upgrade head
```

5. Start Service
```
pipenv run generate
```
