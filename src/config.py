from pathlib import Path


class Config:
    BASE_URL = "http://127.0.0.1:8000"
    sql_lite_db_path: Path = Path("../data/database.db")

    host = "127.0.0.1"
    port = 8000

    SECRET_KEY = "12"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = 30

    headers: dict = {
        "Authorization": ""
    }


cfg = Config()