from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime,timedelta,timezone
from schemas import UsuarioSchema,LoginSchema
from models import Usuario
from dependencias import pegar_session,verificar_token
from main import bcrypt_context,ALGORITMO,ACESSO_TOKEN_EXPIRA_MINUTO,SENHA_SECRETA
from fastapi.security import OAuth2PasswordRequestForm

auth_rota=APIRouter(prefix='/auth',tags=['autenticacao'])

def criar_tokens(id_usuario,duracao_token=timedelta(minutes=ACESSO_TOKEN_EXPIRA_MINUTO)):
    data_expiracao=datetime.now(timezone.utc)+duracao_token
    dict_info = {'sub': id_usuario, 'exp': data_expiracao}
    jwt_codificado=jwt.encode(dict_info,SENHA_SECRETA,ALGORITMO)
    return jwt_codificado

def autenticar_usuario(email,senha,session):
    usuario=session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return  usuario


@auth_rota.get('/')

async def home():

    return {'mensagem':'Você acessou a rota padrão de autenticação','autenticando':False}

@auth_rota.post('/criar_usuario')

async def criar_usuario(usario_schema:UsuarioSchema,session=Depends(pegar_session)):
    usuario=session.query(Usuario).filter(Usuario.email==usario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail='usuario já existente com este email...')
    else:
        senha_criptografada=bcrypt_context.hash(usario_schema.senha)
        novo_usuario=Usuario(usario_schema.nome,usario_schema.email,senha_criptografada,usario_schema.ativo,usario_schema.administrador)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem':f'cadastro realizado com sucesso {usario_schema.email}!'}

@auth_rota.post('/login')
async def login(login_schema:LoginSchema,session:Session=Depends(pegar_session)):
    usuario=autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400,detail='usuario não encotrado ou credencias inválidas')
    else:
        acess_token=criar_tokens(usuario.id_cliente)
        return {
            'acess_token': acess_token,
            'token_type':'Bearer'
        }

@auth_rota.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm=Depends(),session:Session=Depends(pegar_session)):
    usuario=autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
    if not usuario:
        raise HTTPException(status_code=400,detail='usuario não encotrado ou credencias inválidas')
    else:
        acess_token=criar_tokens(usuario.id_cliente)
        refresh_token=criar_tokens(usuario.id_cliente,duracao_token=timedelta(days=7))
        return {
            'acess_token': acess_token,
            'refresh_token':refresh_token,
            'token_type':'Bearer'
        }


@auth_rota.get('/refresh')
async def use_refresh_token(usuario:Usuario=Depends(verificar_token)):
    acess_token=criar_tokens(usuario.id_cliente)
    return {
        'acess_token': acess_token,
        'token_type': 'Bearer'
    }