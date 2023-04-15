import os


class Config:
    postgres_password = os.environ["POSTGRES_PASSWORD"]
    postgres_user = os.environ["POSTGRES_USER"]
    postgres_host = os.environ["POSTGRES_HOST"]
    postgres_port = os.environ["POSTGRES_PORT"]
    postgres_db = os.environ["POSTGRES_DB"]


config = Config()
