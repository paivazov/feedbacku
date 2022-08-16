## First run:
___


### Clone project from git repository
```shell
git clone https://github.com/ITA-Dnipro/Dp-Retraining-Python.git
```

### Setup env files
By the command
```shell
make env
```
or do it manually: create env.local from env.local.sample on your local machine


### Create virtualenv and install requirements
Create virtualenv:
```shell
python -m venv venv
```
And then install requirements:
```shell
pip install -r requirements.txt
```

### Run containers and celery
```shell
make
```
