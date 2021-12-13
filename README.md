# olympus

Olympus Mons UI

## Backend

### Requirements

- A Postgres Instance

```sh
sudo docker run -d -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=U6bwFSLqmBVU90CWwDuRFYL8aiHA_crkuphxZLqw postgres
```

**NOTE: change the database password for production!!!! The env variable `DATABASE_URL` can be used to set it**

(If the instance was already created)

- `docker ps -a` to list all the containers
- `docker restart <container_id>` to restart the database

- Python3.8+

## Usage

- First Time

```sh
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/db_upgrade.sh
```

- After the initial setup

```sh
cd backend
. .venv/bin/activate
python3 main.py
```
