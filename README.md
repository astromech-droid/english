# English

### Quick Install

```sh
git clone -b development https://github.com/astromech-droid/english.git
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata dump/dump.json
```

### Export Data

```sh
python manage.py dumpdata gym -o dump/dump.json
```