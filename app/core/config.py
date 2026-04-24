from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./keys.env")
    
    spotipy_client_id: str
    spotipy_client_secret: str
    spotipy_redirect_uri: str
    api_secret_token: str