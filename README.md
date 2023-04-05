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

### Post Data with API

```python
import requests

url = "https://nyamamotopy.pythonanywhre.com/gym/api/phrases/register"

session = requests.session()
csrftoken = session.get(url).cookies["csrftoken"]

data = {
    "base_en": "test",
    "prpa_en": "testing",
    "pasm_en": "tested",
    "papa_en": "tested",
    "thps_en": "tests",
    "base_ja": "テスト",
    "prpa_ja": "",
    "pasm_ja": "",
    "papa_ja": "",
    "thps_ja": "",
}

headers = {"X-CSRFToken": csrftoken}
response = session.post(url, json=data, headers=headers)
```