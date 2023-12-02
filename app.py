from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from flask_cors import CORS

from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Artistas, ArtistaFilme, Filme
from logger import logger
from schemas import *

info = Info(title="API PUC-Rio", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc.")
filme_tag = Tag(name="Filmes", description="Adição, visualização, edição e remoção de filmes.")
artista_tag = Tag(name="Artistas", description="Adição e edição de artistas com possibilidade de conexão com os filmes.")

@app.get('/', tags=[home_tag])
def home():
    # Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    return redirect('/openapi')

@app.post('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_filme(form: FilmeSchema):
    artistas = []
    for artistas_data in form.artistas:
        artista = Artistas(**artistas_data.dict())
        artistas.append(artista)

    filme = Filme(
        nome=form.nome,
        artistas=artistas,
        resumo=form.resumo,
        imageUrl=form.imageUrl)
    
    logger.debug(f"Adicionando nome do filme: '{filme.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando filme
        session.add(filme)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Nome do filme adicionado com sucesso: '{filme.nome}'")
        return apresenta_filme(filme), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já existe um filme no banco de dados com esse nome."
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"message": error_msg}, 400
    
@app.get('/filmes', tags=[filme_tag], responses={"200": ListagemFilmesSchema, "404": ErrorSchema})

def get_filmes():
    # Faz a busca por todos os filmes cadastrados

    logger.debug(f"Procurando todos os filmes...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filmes = session.query(Filme).all()

    if not filmes:
        # se não há filmes cadastrados
        return {"Não há nenhum filme com esse nome no nosso banco de dados!": []}, 200
    else:
        logger.debug(f"%d filmes encontrados no nosso banco de dados!" % len(filmes))
        # retorna a representação de filmes
        print(filmes)
        return apresenta_filmes(filmes), 200
    
@app.get('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema})

def get_filme(query: FilmeBuscaSchema):
    # Faz a busca por um filme a partir do id
    
    filme_id = query.id
    logger.debug(f"Procurando todos os filmes... #{filme_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filme = session.query(Filme).filter(Filme.id == filme_id).first()

    if not filme:
        # se o filme não foi encontrado
        error_msg = "Não há nenhum filme com esse nome no nosso banco de dados!"
        logger.warning(f"Erro ao buscar o filme desejado.'{filme_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Filmes com a seguinte pesquisa encontrados: '{filme.nome}'")
        return apresenta_filme(filme), 200
    
@app.delete('/filme', tags=[filme_tag], responses={"200": FilmeDeleteSchema, "404": ErrorSchema})

def delete_filme(query: FilmeBuscaSchema):
    # Deleta um filme a partir do nome de filme informado

    filme_nome = unquote((query.nome))
    print(filme_nome)
    logger.debug(f"Deletando dados sobre o filme {filme_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Filme).filter(Filme.nome == filme_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"O filme {filme_nome} foi deletado com sucesso!")
        return {"message": "Filme removido", "id": filme_nome}
    else:
        # se o filme não foi encontrado
        error_msg = "Não há nenhum filme com esse nome no nosso banco de dados!"
        logger.warning(f"Erro ao deletar o filme '{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404
    
@app.put('/filme/<int:filme_id>', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def edit_filme(filme_id: int, form: FilmeSchema):

    try:
        # criando conexão com a base
        session = Session()
        # buscando filme pelo id
        filme = session.query(Filme).filter(Filme.id == filme_id).first()

        if not filme:
            # se o filme não foi encontrado
            error_msg = "Não há nenhum filme com esse ID no nosso banco de dados!"
            logger.warning(f"Erro ao editar o filme #{filme_id}, {error_msg}")
            return {"message": error_msg}, 404

        # atualizando as informações do filme se existirem nos dados fornecidos
        if form.nome:
            filme.nome = form.nome
        if form.resumo:
            filme.resumo = form.resumo
        if form.imageUrl:
            filme.imageUrl = form.imageUrl

        # removendo artistas antigos
        filme.artistas = []

        # adicionando novos artistas
        if form.artistas:
            for artistas_data in form.artistas:
                artista = Artistas(**artistas_data.dict())
                filme.artistas.append(artista)

        # efetivando as mudanças
        session.commit()

        logger.debug(f"Filme #{filme_id} editado com sucesso!")
        return apresenta_filme(filme), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao editar o filme #{filme_id}, {error_msg}")
        return {"message": error_msg}, 400
    
@app.post('/artista', tags=[artista_tag], responses={"200": ArtistaViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_artista(form: ArtistasSchema):
    filmes = []
    for filmes_data in form.filmes:
        filme = Filme(**filmes_data.dict())
        filmes.append(filme)

    artista = Artistas(
        nome=form.nome,
        filmes=filmes,
        resumo=form.resumo,
        imageUrl=form.imageUrl)
    
    logger.debug(f"Adicionando nome do artista: '{artista.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando artista
        session.add(artista)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Nome do artista adicionado com sucesso: '{artista.nome}'")
        return apresenta_artista(artista), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já existe um artista no banco de dados com esse nome."
        logger.warning(f"Erro ao adicionar o artista '{artista.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao adicionar o artista '{artista.nome}', {error_msg}")
        return {"message": error_msg}, 400
    
@app.get('/artistas', tags=[artista_tag], responses={"200": ListagemArtistaSchema, "404": ErrorSchema})

def get_artistas():

    logger.debug(f"Procurando todos os artistas...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    artistas = session.query(Artistas).all()

    if not artistas:
        return {"Não há nenhum artista com esse nome no nosso banco de dados!": []}, 200
    else:
        logger.debug(f"%d artistas encontrados no nosso banco de dados!" % len(artistas))
        print(artistas)
        return apresenta_artistas(artistas), 200
    
@app.delete('/artista', tags=[artista_tag], responses={"200": ArtistaDeleteSchema, "404": ErrorSchema})

def delete_artista(query: ArtistaBuscaSchema):

    artista_nome = unquote((query.nome))
    print(artista_nome)
    logger.debug(f"Deletando dados sobre o artista {artista_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Artistas).filter(Artistas.nome == artista_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"O artista {artista_nome} foi deletado com sucesso!")
        return {"message": "Artista removido", "id": artista_nome}
    else:
        # se o artista não foi encontrado
        error_msg = "Não há nenhum artista com esse nome no nosso banco de dados!"
        logger.warning(f"Erro ao deletar o artista '{artista_nome}', {error_msg}")
        return {"message": error_msg}, 404
    
@app.put('/artista/<int:artista_id>', tags=[artista_tag], responses={"200": ArtistaViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def edit_artista(artista_id: int, form: ArtistasSchema):

    try:
        # criando conexão com a base
        session = Session()
        # buscando artista pelo id
        artista = session.query(Artistas).filter(Artistas.id == artista_id).first()

        if not artista:
            # se o artista não foi encontrado
            error_msg = "Não há nenhum artista com esse ID no nosso banco de dados!"
            logger.warning(f"Erro ao editar o artista #{artista_id}, {error_msg}")
            return {"message": error_msg}, 404

        # atualizando as informações do artista se existirem nos dados fornecidos
        if form.nome:
            artista.nome = form.nome

        # removendo filmes antigos
        artista.filmes = []

        # adicionando novos filmes
        if form.filmes:
            for filmes_data in form.filmes:
                filme = Filme(**filmes_data.dict())
                artista.filmes.append(filme)

        # efetivando as mudanças
        session.commit()

        logger.debug(f"Artista #{artista_id} editado com sucesso!")
        return apresenta_artista(artista), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao editar o artista #{artista_id}, {error_msg}")
        return {"message": error_msg}, 400