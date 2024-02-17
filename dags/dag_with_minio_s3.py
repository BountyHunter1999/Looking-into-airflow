from datetime import datetime, timedelta

from airflow import DAG

# get the version by going into the scheduler's shell
# to get the amazon version `pip list | grep amazon`: apache-airflow-providers-amazon          8.16.0
# https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.16.0/_api/airflow/providers/amazon/aws/sensors/s3/index.html
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {"owner": "mikeyy", "retries": 5, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="dag_with_minio_s3_v1",
    start_date=datetime(2024, 2, 16),
    schedule_interval="@daily",
    default_args=default_args,
) as dag:
    # get access keys from minio
    # {
    #   "aws_access_key_id": "eEI5RH3k8PMmOm4lju0R",
    #   "aws_secret_access_key": "1pgTwb80E1VOxK8d6eifwfgfL1mqz7NfQwsCgGKs",
    #   "endpoint_url": "http://host.docker.internal:9000" # as run from docker desktop
    # }
    task1 = S3KeySensor(
        task_id="sensor_minio_s3",
        bucket_name="test123",
        bucket_key="data.csv",
        # add the connection from airflow add connection
        aws_conn_id="minio_airflow",
        # aws_conn_id="minio_root_access",
        # poke to see if the file is there, if it is the task is a success
        mode="poke",
        poke_interval=5,
        timeout=30,
    )
