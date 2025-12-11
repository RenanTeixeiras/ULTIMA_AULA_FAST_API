# models.py
from pydantic import BaseModel, Field
from typing import Optional

class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    ano: Optional[int] = Field(None, ge=1440, le=2026)
    isbn: Optional[str] = None

class LivroResponse(LivroCreate):
    id: int
    titulo: str
    autor: str
    ano: int
    criado_em: str