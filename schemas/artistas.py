from pydantic import BaseModel
from typing import List, Optional
from model.artistas import Artistas

from schemas import FilmeSchema

class ArtistasSchema(BaseModel):
    nome: str
    filmes: Optional[List[FilmeSchema]]

    class Config:
        orm_mode = True

class ArtistaBuscaSchema(BaseModel):
    nome: str

class ListagemArtistaSchema(BaseModel):
    artistas: List[ArtistasSchema]

def apresenta_artistas(artistas: List[Artistas]):
    result = []
    for artista in artistas:
        result.append({
            "nome": artista.nome,
            "filmes": artista.filmes,
        })

    return {"artistas": result}

class ArtistaViewSchema(BaseModel):
    id: int = 1
    nome: str = "Will Smith"
    total_filmes: int = 1
    filmes:List[FilmeSchema]

class ArtistaDeleteSchema(BaseModel):
    message: str
    nome: str

def apresenta_artista(artista: Artistas):
    return {
        "id": artista.id,
        "nome": artista.nome,
        "total_filmes": len(artista.filmes),
        "filmes": [{"texto": c.texto} for c in artista.filmes]
    }