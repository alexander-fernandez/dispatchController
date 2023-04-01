
## Instructions

### Python Notes (project from scratch)
    $ python -m venv .venv
    $ python -m pip install --upgrade pip
    # Windows
    $ .\.venv\Scripts\activate.ps1
    # Linux 
    $ source env/bin/activate
    $ pip install -r requirements.txt

### Build
    $ cd dispatchController
    $ docker compose build

### Run
    $ docker compose up -d

### Stop
    $ docker compose stop

### Endpoints

#### - registering a drone;

curl --location --request POST 'http://127.0.0.1:5000/drone' --header 'Content-Type: pplication/json' --data-raw '{"battery": 100, "max_weight": 490, "model": "Heavyweight", "serial": "18861093-33a8-46da-9d75-71c339fe41d8"}'

#### - loading a drone with medication items;

curl --location --request POST 'http://127.0.0.1:5000/drone/2dfcfb09-a3c4-4ffc-a98a-50fee3c2228e/load'

#### - checking loaded medication items for a given drone;

curl --location --request GET 'http://127.0.0.1:5000/drone/2dfcfb09-a3c4-4ffc-a98a-50fee3c2228e/load'

#### - checking available drones for loading;

curl --location --request GET 'http://127.0.0.1:5000/drone/available'

#### - check drone battery level for a given drone;

curl --location --request GET 'http://127.0.0.1:5000/drone/2dfcfb09-a3c4-4ffc-a98a-50fee3c2228e/battery'
