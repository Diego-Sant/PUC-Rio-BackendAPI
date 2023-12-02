from pydantic import BaseModel
from typing import List

from schemas import FilmeSchema

class ArtistasSchema(BaseModel):
    nome: str
    filmes: List[FilmeSchema]

    class Config:
        orm_mode = True