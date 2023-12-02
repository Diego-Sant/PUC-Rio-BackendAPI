from pydantic import BaseModel
from typing import Optional, List
from model.filme import Filme

from schemas import ArtistasSchema

class FilmeSchema(BaseModel):
    nome: str
    artistas: Optional[List[ArtistasSchema]]
    resumo: str
    imageUrl: str

    class Config:
        orm_mode = True

class FilmeBuscaSchema(BaseModel):
    #Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no nome do filme.
    nome: str

class ListagemFilmesSchema(BaseModel):
    filmes: List[FilmeSchema]

def apresenta_filmes(filmes: List[Filme]):
    # Retorna uma representação do filme seguindo o schema definido em FilmeViewSchema.
    
    result = []
    for filme in filmes:
        result.append({
            "nome": filme.nome,
            "artistas": filme.artistas,
            "resumo": filme.resumo,
            "imageUrl": filme.imageUrl
        })

    return {"filmes": result}

class FilmeViewSchema(BaseModel):
    id: int = 1
    nome: str = "Homem-Aranha: Sem Volta para Casa"
    resumo: str = "Com a identidade do Homem-Aranha revelada, para restabelecer seu segredo, Peter Parker pede ajuda ao Doutor Estranho. O feitiço do mago, porém, corre mal e acaba trazendo vilões do Homem-Aranha de outros universos."
    imageUrl: str = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2/fVzXp3NwovUlLe7fvoRynCmBPNc.jpg"
    total_artistas: int = 1
    artistas:List[ArtistasSchema]

class FilmeDeleteSchema(BaseModel):
    # Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    message: str
    nome: str

def apresenta_filme(filme: Filme):
    # Retorna uma representação do filme seguindo o schema definido em FilmeViewSchema.
    
    return {
        "id": filme.id,
        "nome": filme.nome,
        "resumo": filme.resumo,
        "imageUrl": filme.imageUrl,
        "total_artistas": len(filme.artistas),
        "artistas": [{"texto": c.texto} for c in filme.artistas]
    }