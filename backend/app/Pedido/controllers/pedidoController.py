from fastapi import APIRouter, Depends
from app.Pedido.services.pedidoService import PedidoService
from app.Pedido.schemas.pedidoSchemas import *
from app.database import obtenerSesion
from app.configuracionGeneral.seguridadJWT import protegerRuta
from app.configuracionGeneral.schemasGenerales import respuestaApi

router = APIRouter()

@router.get("/", tags=["Pedido"], summary="Obtener todos los pedidos", status_code=200, response_model=respuestaApi,
            description="Lista todos los pedidos. Roles permitidos: Administrador, Bodeguero. Útil para ver el historial y estado de pedidos (devuelve información completa del usuario creador, aprobador, productos y detalles).")
async def listarPedidos(dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "GET"))):
    return PedidoService(dbSession).listarPedidos()

@router.get("/pendientes", tags=["Pedido"], summary="Obtener pedidos pendientes de revisión", status_code=200, response_model=respuestaApi,
            description="Devuelve pedidos con estado 'PENDIENTE_REVISION'. Roles: Administrador, Bodeguero. Útil para Administrador para revisar y aprobar/rechazar solicitudes.")
async def listarPedidosPendientes(dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "GET"))):
    return PedidoService(dbSession).listarPedidosPendientes()

@router.get("/{idPedido}", tags=["Pedido"], summary="Obtener un pedido por id", status_code=200, response_model=respuestaApi,
            description="Devuelve un pedido por su id con detalles y datos de usuarios. Roles: Administrador, Bodeguero.")
async def obtenerPedido(idPedido: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "GET"))):
    return PedidoService(dbSession).obtenerPorId(idPedido)

@router.post("/", tags=["Pedido"], summary="Crear un nuevo pedido", status_code=201, response_model=respuestaApi,
            description="Crear un pedido. Enviar: {detalles: [{idProducto, cantidadSolicitada}]}. El pedido se crea en estado 'PENDIENTE_REVISION'. Roles: Bodeguero (usa para solicitar abastecimiento) y Administrador.")
async def crearPedido(pedido: PedidoCrearSchema, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "POST"))):
    return PedidoService(dbSession).crearPedido(pedido, usuario)

@router.post("/{idPedido}/revisar", tags=["Pedido"], summary="Revisar/aprobar/rechazar un pedido", status_code=200, response_model=respuestaApi,
            description="Aprobar o rechazar un pedido. Enviar: {estadoPedido: 'APROBADO'|'RECHAZADO', observaciones?: string}. Solo el Administrador puede aprobar pedidos creados por otros usuarios.")
async def revisarPedido(idPedido: int, revisar: RevisarPedidoSchema, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "ALL"))):
    return PedidoService(dbSession).revisarPedido(idPedido, revisar, usuario)

# Detalles
@router.get("/{idPedido}/detalles", tags=["Pedido"], summary="Listar detalles de un pedido", status_code=200, response_model=respuestaApi,
            description="Listar todos los detalles de un pedido. Roles: Administrador, Bodeguero.")
async def listarDetalles(idPedido: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "GET"))):
    return PedidoService(dbSession).listarDetallesPorPedido(idPedido)

@router.get("/detalles/{idDetalle}", tags=["Pedido"], summary="Obtener un detalle por id", status_code=200, response_model=respuestaApi,
            description="Obtener un detalle de pedido por su id con información del producto y usuario receptor. Roles: Administrador, Bodeguero.")
async def obtenerDetalle(idDetalle: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "GET"))):
    return PedidoService(dbSession).obtenerDetallePorId(idDetalle)

@router.post("/detalles/{idDetalle}/recepcionar", tags=["Pedido"], summary="Confirmar recepción de un detalle de pedido", status_code=200, response_model=respuestaApi,
            description="Confirmar recepción completa de un detalle: enviar {confirmar: true}. Al confirmar, el detalle se marca como 'RECIBIDO' y la cantidad solicitada se suma al inventario. Roles: Bodeguero (si el pedido está aprobado) y Administrador.")
async def recepcionarDetalle(idDetalle: int, recepcion: RecepcionDetalleSchema, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Pedido", "POST"))):
    return PedidoService(dbSession).realizarRecepcionDetalle(idDetalle, recepcion, usuario)
