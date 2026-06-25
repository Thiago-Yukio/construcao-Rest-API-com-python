from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SENHA_SECRETA=os.getenv('SENHA_SECRETA')
ALGORITMO=os.getenv('ALGORITMO')
ACESSO_TOKEN_EXPIRA_MINUTO=int(os.getenv('ACESSO_TOKEN_EXPIRA_MINUTO'))

aplicativo=FastAPI()
#Para rodar o codigo executar: uvicorn main:aplicativo --reload

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_schema=OAuth2PasswordBearer(tokenUrl='auth/login_form')

from auth_rotas import auth_rota
from ordens_rotas import ordem_rota

#Incluido rota no sistema
aplicativo.include_router(auth_rota)
aplicativo.include_router(ordem_rota)