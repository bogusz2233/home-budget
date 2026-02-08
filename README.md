# home-budget
This repository stores scripts used to support home budget maintaining.

# Setup

## Virtual envirement
First of all you have to install and setup virtual envirement [venv](https://docs.python.org/3/library/venv.html).

If you have it installed run following commands to create and active venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies
Once you have virtual envirement setup you can install all dependencies by using command:
```bash
pip install -e .
```

## Run API + UI
Start the FastAPI server (serves the frontend at `/`):
```bash
uvicorn home_budget.app:app --reload
```

Open http://localhost:8000 to view the UI. The API is under `/api`.