from pathlib import Path


class Config:
    BASE_URL = "http://127.0.0.1:8000"
    sql_lite_db_path: Path = Path("../data/database.db")


cfg = Config()