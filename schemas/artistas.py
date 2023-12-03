from pydantic import BaseModel
from typing import List, Optional
from model.artistas import Artistas

class ArtistasSchema(BaseModel):
    nome: str
    idade: int
    imageUrl: str

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
            "idade": artista.idade,
        })

    return {"artistas": result}

class ArtistaViewSchema(BaseModel):
    id: int = 1
    nome: str = "Will Smith"
    idade: int = 35
    imageUrl: str = "https://www.themoviedb.org/t/p/w300_and_h450_bestv2/qgjMfefsKwSYsyCaIX46uyOXIpy.jpg"

class ArtistaDeleteSchema(BaseModel):
    message: str
    nome: str

def apresenta_artista(artista: Artistas):
    return {
        "id": artista.id,
        "nome": artista.nome,
        "idade": artista.idade,
        "imageUrl": artista.imageUrl
    }