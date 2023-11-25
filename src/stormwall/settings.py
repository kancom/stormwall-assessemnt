from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    listen_ports: str = "8000"
    intervals: str = "10,60"
    sync_interval: int = 70
    output_file: str = "stats"
