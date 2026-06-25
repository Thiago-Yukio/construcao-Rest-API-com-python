from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    administrador:Optional[bool]

    class Config:
        from_attributes=True

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes=True

class LoginSchema(BaseModel):
    email:str
    senha:str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    origem_fabricado:str
    preco_unitario:float
    descricao:str

    class Config:
        from_attributes = True

class ResponstaPedidoSchema(BaseModel):
    id_pedido: int
    status: str
    preco: float
    itens: list[ItemPedidoSchema]

    class Config:
        from_attributes = True