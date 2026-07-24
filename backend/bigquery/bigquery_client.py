from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from util import load_setting

def get_bigquery_client():
    credentials = Credentials.from_service_account_file(load_setting.KEY_GCP)
    return bigquery.Client(
        project=load_setting.PROJECT_ID,
        credentials=credentials,
    )
client = get_bigquery_client()

def execute(query: str, parameters = None):
    job_config = bigquery.QueryJobConfig(
        query_parameters=parameters or []
    )
    return list(client.query(query, job_config=job_config).result())