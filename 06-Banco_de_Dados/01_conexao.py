import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

database = sqlite3.connect(ROOT_PATH / "banco_de_dados.db")
cursor = database.cursor()

cursor.execute(
    "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "nome VARCHAR(100), email VARCHAR(150))"
)
