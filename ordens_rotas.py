from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencias import pegar_session,verificar_token
from schemas import PedidoSchema,ItemPedidoSchema,ResponstaPedidoSchema
from models import Pedido, Usuario,ItemPedido

ordem_rota=APIRouter(prefix='/ordem',tags=['pedido'],dependencies=[Depends(verificar_token)])

@ordem_rota.get('/')

async def pedido():

    return {'mensagem':'Você acessou a rota de pedidos'}

@ordem_rota.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema,session:Session=Depends(pegar_session)):
    novo_pedido=Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {'mensagem':f'Pedido aprovado. ID do pedido: {novo_pedido.id_pedido}'}

@ordem_rota.post('/pedido/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido:int,session:Session=Depends(pegar_session),usuario:Usuario=Depends(verificar_token)):

    pedido=session.query(Pedido).filter(Pedido.id_pedido==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400,detail='Pedido não encontrado')
    if not usuario.administrador and usuario.id_cliente!=pedido.usuario:
        raise HTTPException(status_code=403,detail='Você não tem autorização para realizar essa modificação')

    pedido.status='CANCELADO'
    session.commit()
    return {
        'mensagem': f'Pedido número {id_pedido} cancelado com sucesso!',
        'pedido':pedido
    }

@ordem_rota.get('/liste')
async def listar_pedido(session:Session=Depends(pegar_session),usuario:Usuario=Depends(verificar_token)):
    if usuario.administrador==False:
        raise HTTPException(status_code=401,detail='Você não tem autorização para realizar essa modificação')
    else:
        pedido=session.query(Pedido).all()
        return {
            'pedidos':pedido
        }

@ordem_rota.post('/pedido/adicionar-item/{id_pedido}')
async  def adicionar_item_pedido(id_pedido:int, item_pedido_schema:ItemPedidoSchema,session:Session=Depends(pegar_session),usuario:Usuario=Depends(verificar_token)):
    pedido=session.query(Pedido).filter(Pedido.id_pedido==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400,detail='Pedido não existente')
    if not usuario.administrador and usuario.id_cliente != pedido.usuario:
        raise HTTPException(status_code=401,detail='Você não tem autorização para realizar essa modificação')
    item_pedido = ItemPedido(
        origem_fabricado=item_pedido_schema.origem_fabricado,
        descricao=item_pedido_schema.descricao,
        preco_unitario=item_pedido_schema.preco_unitario,
        pedido=id_pedido,
        quantidade=item_pedido_schema.quantidade
    )
    session.add(item_pedido)
    session.flush()
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem':'Item criado com sucesso',
        'item_id':item_pedido.id_item_pedido,
        'preco_pedido':pedido.preco
    }


@ordem_rota.post('/pedido/remover-item/{id_item_pedido}')
async  def remover_item_pedido(id_item_pedido:int,session:Session=Depends(pegar_session),usuario:Usuario=Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id_item_pedido == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400,detail='Item no pedido não existente')
    pedido = session.query(Pedido).filter(Pedido.id_pedido == item_pedido.pedido).first()
    if not usuario.administrador and usuario.id_cliente != pedido.usuario:
        raise HTTPException(status_code=401,detail='Você não tem autorização para realizar essa modificação')
    session.delete(item_pedido)
    session.flush()
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem':'Item removido com sucesso',
        'quantidade_itens_pedidos':len(pedido.itens),
        'pedido':pedido
    }

@ordem_rota.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido:int,session:Session=Depends(pegar_session),usuario:Usuario=Depends(verificar_token)):
    pedido=session.query(Pedido).filter(Pedido.id_pedido==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400,detail='Pedido não encontrado')
    if not usuario.administrador and usuario.id_cliente!=pedido.usuario:
        raise HTTPException(status_code=401,detail='Você não tem autorização para realizar essa modificação')
    pedido.status='FINALIZADO'
    session.commit()
    return {
        'mensagem': f'Pedido número {id_pedido} FINALIZADO com sucesso!',
        'pedido':pedido
    }

@ordem_rota.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_session), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id_pedido==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.administrador and usuario.id_cliente != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

#Visualização dos pedidos de um unico usuario
@ordem_rota.get("/listar/pedidos-usuario",response_model=list[ResponstaPedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_session), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id_cliente).all()
    return pedidos