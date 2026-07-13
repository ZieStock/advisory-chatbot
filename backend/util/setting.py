from pydantic_settings import BaseSettings
class Setting(BaseSettings):
    DATABASE: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    VM_IP: str
    MILVUS_HOST: str
    MILVUS_PORT: str
    KEY_GCP: str
    PROJECT_ID: str
    BIGQUERY_DATASET: str
    model_config = {
        'env_file': ".env"
    }
load_setting = Setting()