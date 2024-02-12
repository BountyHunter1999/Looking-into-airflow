from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {"owner": "Mikeyy", "retries": 5, "retry_delay": timedelta(minutes=5)}

with DAG(
    dag_id="dag_with_postgres_operator",
    default_args=default_args,
    start_date=datetime(2024, 2, 11),
    schedule_interval="0 0 * * *",
) as dag:
    task1 = PostgresOperator(
        task_id="create_pg_table",
        postgres_conn_id="postgres_try",
        sql="""
        CREATE TABLE IF NOT EXISTS dag_runs (
            dt date,
            dag_id character varying,
            primary key (dt, dag_id)
        )
        """,
    )

    task2 = PostgresOperator(
        task_id="insert_into_table",
        postgres_conn_id="postgres_try",
        # ds = execution date
        sql="""
        INSERT INTO dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """,
    )

    # delete before insert to avoid primary key violation in airflow
    task3 = PostgresOperator(
        task_id="delete_from_table",
        postgres_conn_id="postgres_try",
        # ds = execution date
        sql="""
        DELETE FROM dag_runs WHERE dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}')
        """,
    )
    task1 >> task3 >> task2
