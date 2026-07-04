from pydantic_settings import BaseSettings
class Setting(BaseSettings):
    DATABASE: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    VM_IP: str
    model_config = {
        'env_file': ".env"
    }
load_setting = Setting()