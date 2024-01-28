# Looking-into-airflow

## Installation

### PyPI

- [PyPI](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
  `pip install "apache-airflow[celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.10.txt"` match the constraints version with the python version we have
- `export AIRFLOW_HOME=${PWD}` (default is airflow directory on home)
- `airflow db init` initialize the db
  - create sqlite database
  - a log folder and,
  - some configuration files
- `airflow webserver -p 8080` start the airflow webserver
- `pip install virtualenv`: PythonVirtualenvOperator requires virtualenv

### Creating User

- just doing `airflow users create` will give the structure to follow

```
airflow users create \
          --username test123 \
          --firstname mr_test \
          --lastname okay \
          --role Admin \
          --email admin@example.org
```

- `password: admin123`
- start the airflow webserver and login with the provided credentials

### Create scheduler

- we need a scheduler in order to execute the DAG (Directed Acyclic Graph), a conceptual representation of a series of activities
  - each circle represents an activity, some of which are connected by lines representing the flow from one activity to another
-
