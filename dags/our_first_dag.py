from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "mikeyy", "retries": 5, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="our_1st_dag_v5",
    default_args=default_args,
    description="This was our first dag that we wrote",
    start_date=datetime(2024, 2, 2, 2),
    schedule_interval="@daily",
) as dag:
    task1 = BashOperator(
        task_id="1st_task", bash_command="echo hello world, this is the 1st task!"
    )
    task2 = BashOperator(
        task_id="2nd_task", bash_command="echo I am task 2 and I run after task 1!"
    )
    task3 = BashOperator(
        task_id="3nd_task",
        bash_command="echo I am task 3 and I run after task 1 same as task 1!",
    )

    # Task dependency method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    # Task dependency method 2, bit shift operator to create dependency
    # task1 >> task2
    # task1 >> task3

    # Task dependency method 3
    task1 >> [task2, task3]
