from pydantic import BaseModel
from typing import List, Optional
from model.artistas import Artistas

class ArtistasSchema(BaseModel):
    nome: str = "Cillian Murphy"
    idade: int = 47
    imageUrl: str = "https://www.themoviedb.org/t/p/w300_and_h450_bestv2/dm6V24NjjvjMiCtbMkc8Y2WPm2e.jpg"

    class Config:
        orm_mode = True

class ArtistaBuscaSchema(BaseModel):
    nome: str = "Cillian Murphy"

class ListagemArtistaSchema(BaseModel):
    artistas: List[ArtistasSchema]

def apresenta_artistas(artistas: List[Artistas]):
    result = []
    for artista in artistas:
        result.append({
            "nome": artista.nome,
            "idade": artista.idade,
            "imageUrl": artista.imageUrl
        })

    return {"artistas": result}

class ArtistaViewSchema(BaseModel):
    id: int = 1
    nome: str = "Robert Downey Jr."
    idade: int = 58
    imageUrl: str = "https://www.themoviedb.org/t/p/w300_and_h450_bestv2/im9SAqJPZKEbVZGmjXuLI4O7RvM.jpg"

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