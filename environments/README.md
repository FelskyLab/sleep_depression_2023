# Environments

Using environments helps others reproduce your work by providing them the same software, versions, and environmental configuration that you use in your project.

Always use them when you can.

## Python

### .env

If you have any specific bash shell environment configurations that are necessary for you project to run then place them within `.env` and load them as follows in python.

```python
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)
```


### poetry

Contains a virtual environment created with [`venv`](https://docs.python.org/3/library/venv.html) that contains [`poetry`](https://python-poetry.org) a python package and dependency manager

```bash
make poetry
```

All python packages subsequently installed with `pip` will be isolated from the system and user-wide packages. This allows you to manage dependencies on a per project basis to avoid future conflicts.

If you want to make the most of `poetry` run the following commands:

```bash
make init
make activate
```

For help type `poetry`

### [requirements.txt](https://pip.pypa.io/en/latest/user_guide/#requirements-files)

Adding your project's python package dependencies to a `requirements.txt` file will enable repeatable creation of the virtual environment you used for your project.

This can be accomplished by executing the following.

```bash
(venv)$ python3 -m pip freeze > environments/requirements.txt
```

For another person who has pulled your project from a version control system they can then reproduce your environment with the following

```bash
python3 -m venv environments/venv
source environments/venv/bin/activate
(venv)$ python3 -m pip install -r environments/requirements.txt
```

## conda

### mamba

