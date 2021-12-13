# Evmos Testnet Rewards

## Requirements

- A Postgres Instance

```sh
sudo docker run -d -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=U6bwFSLqmBVU90CWwDuRFYL8aiHA_crkuphxZLqw postgres
```

- Python3.8+

## Usage

- First Time

```sh
cd testnetrewards
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/db_upgrade.sh
```

- After the initial setup

```sh
cd testnetrewards
. .venv/bin/activate
python3 main.py
```
