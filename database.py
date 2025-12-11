# database.py
import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "biblioteca.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    try:
        yield conn
    finally:
        conn.close()

def criar_tabela():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano INTEGER,
                isbn TEXT UNIQUE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()