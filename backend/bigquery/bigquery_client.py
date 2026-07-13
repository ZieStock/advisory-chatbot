from google.cloud import bigquery
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from util import load_setting

def get_bigquery_client():
    credentials = Credentials.from_service_account_file(load_setting.KEY_GCP)
    return bigquery.Client(
        project=load_setting.PROJECT_ID,
        credentials=credentials,
    )
client = get_bigquery_client()