# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from typing import List
from models import LivroCreate, LivroResponse
from database import get_db, criar_tabela

@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabela()
    print("Banco de dados pronto – tabela 'livros' criada se necessário")
    yield

app = FastAPI(
    title="API de Livros",
    description="CRUD completo de livros com SQLite",
    version="2.0",
    lifespan=lifespan
)

# POST – já existia
@app.post("/livros/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate):
    sql = "INSERT INTO livros (titulo, autor, ano, isbn) VALUES (?, ?, ?, ?)"
    try:
        with get_db() as conn:
            cursor = conn.execute(sql, (livro.titulo, livro.autor, livro.ano, livro.isbn))
            conn.commit()
            livro_id = cursor.lastrowid

        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
            return dict(cursor.fetchone())

    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            raise HTTPException(status_code=400, detail="ISBN já cadastrado")
        raise HTTPException(status_code=400, detail="Erro ao salvar livro")

# GET todos os livros
@app.get("/livros/", response_model=List[LivroResponse])
def listar_todos_os_livros():
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM livros ORDER BY criado_em DESC")
        livros = [dict(row) for row in cursor.fetchall()]
        return livros

# GET livro por ID
@app.get("/livros/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int):
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        livro = cursor.fetchone()
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return dict(livro)