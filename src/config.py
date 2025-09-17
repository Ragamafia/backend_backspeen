from pathlib import Path


class Config:
    base_url = "http://127.0.0.1:8000"
    sql_lite_db_path: Path = Path("../data/database.db")
    host = "127.0.0.1"
    port = 8000

    admin_name = "Admin"
    admin_last_name = "Admin"
    admin_email = "admin@admin.com"
    admin_password = "654321"

    secret_key = "12"
    algorithm = "HS256"

    headers: dict = {
        "Authorization": ""
    }

    def __init__(self):
        super().__init__()
        self.sql_lite_db_path.parent.mkdir(parents=True, exist_ok=True)


cfg = Config()
