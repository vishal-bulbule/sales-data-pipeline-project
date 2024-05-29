import functions_framework
from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig
import time

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    filename = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {filename}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")
    load_bq(filename)


dataset = 'sales'
table = 'orders'
def load_bq(filename):
    client = bigquery.Client()
    filename = filename
    table_ref = client.dataset(dataset).table(table)
    job_config = LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    uri = f'gs://bkt-sales-data/{filename}'
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  
    time.sleep(10)
    num_rows = load_job.output_rows
    print(f"{num_rows} rows loaded into {table}.")