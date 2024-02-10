from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {"owner": "mikeyy", "retries": 5, "retry_delay": timedelta(minutes=5)}


# def greet(age, ti):
def greet(ti):
    """ti can only call xcoms"""
    # name = ti.xcom_pull(task_ids="get_name")  # pull the return value from that task
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age", key="age")
    print(
        f"Hello World! My name is {first_name} {last_name}, "
        f"and I am {age} years old!"
    )


def get_name(ti):
    # return "Mikeyy"
    ti.xcom_push(key="first_name", value="Mikeyy")
    ti.xcom_push(key="last_name", value="Gonzales")


def get_age(ti):
    ti.xcom_push(key="age", value=32)


with DAG(
    default_args=default_args,
    dag_id="dag_with_python",
    description="1st DAG with python operator",
    start_date=datetime(2024, 2, 3),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        # op_kwargs={"age": 30}
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age,
    )

    # return value will be pushed to xcoms (admin > xcoms)
    [task2, task3] >> task1
