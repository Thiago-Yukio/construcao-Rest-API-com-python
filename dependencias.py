from sqlalchemy.orm import sessionmaker,Session
from models import db,Usuario
from fastapi import Depends,HTTPException
from jose import jwt,JWTError
from main import SENHA_SECRETA,ALGORITMO,oauth2_schema

def pegar_session():
    try:
        Session=sessionmaker(bind=db)
        session=Session()
        yield session
    finally:
        session.close()

def verificar_token(token:str=Depends(oauth2_schema),session:Session=Depends(pegar_session)):
    try:
        dict_info=jwt.decode(token,SENHA_SECRETA,ALGORITMO)
        id_usuario=dict_info.get('sub')
    except JWTError:
        raise HTTPException(status_code=401,detail='Acesso Negado, verifique a validade de token')
    usuario=session.query(Usuario).filter(Usuario.id_cliente==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401,detail='Acesso Negado')
    return usuario