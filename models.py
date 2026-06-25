from sqlalchemy import create_engine,Column,String,Integer,Boolean,Float,ForeignKey
from sqlalchemy.orm import declarative_base, relationship

#cria a conexão do seu banco
db=create_engine('sqlite:///banco.db')

#cria a base de banco de dados
base=declarative_base()

#cria as classes/tabelas do banco
class Usuario(base):
    __tablename__='usuarios'
    id_cliente=Column('id_cliente',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    email=Column('email',String,nullable=False,unique=True)
    senha=Column('senha',String,nullable=False)
    ativo=Column('ativo',Boolean)
    administrador=Column('administrador',Boolean,default=False)

    def __init__(self,nome,email,senha,ativo=True,administrador=False):
        self.nome=nome
        self.email=email
        self.senha=senha
        self.ativo=ativo
        self.administrador=administrador

class Pedido(base):
    __tablename__ = 'pedidos'
    ''' 
    STATUS_PEDIDO=(
    ('PENDENTE','PENDENTE'),
    ('CANCELADO','CANCELADO'),
    ('FINALIZADO','FINALIZADO')
    )'''
    id_pedido=Column('id_pedido',Integer,primary_key=True,autoincrement=True)
    status = Column('status',String,default='PENDENTE')
    usuario = Column('usuario',ForeignKey('usuarios.id_cliente'),nullable=False)
    preco=Column('preco',Float,nullable=False,default=0.0)
    itens=relationship('ItemPedido',cascade='all,delete')

    def __init__(self,usuario,preco=0,status='PENDENTE'):
        self.usuario=usuario
        self.preco=preco
        self.status=status

    def calcular_preco(self):
        preco_pedido = 0
        for item in self.itens:
            preco_pedido += item.preco_unitario * item.quantidade
        self.preco = preco_pedido
        return self.preco

class ItemPedido(base):
    __tablename__ = 'item_pedido'

    id_item_pedido = Column('id_item_pedido',Integer,primary_key=True,autoincrement=True)
    quantidade=Column('quantidade',Integer,nullable=False)
    origem_fabricado=Column('origem_fabricado',String)
    preco_unitario=Column('preco_unitario',Float,nullable=False)
    descricao=Column('descricao',String)
    pedido = Column('pedido',ForeignKey(Pedido.id_pedido),nullable=False)

    def __init__(self,origem_fabricado,descricao,preco_unitario,pedido,quantidade=1):
        self.quantidade=quantidade
        self.origem_fabricado=origem_fabricado
        self.preco_unitario=preco_unitario
        self.descricao=descricao
        self.pedido=pedido

#executado a criação dos metadados do seu banco
base.metadata.create_all(bind=db)
