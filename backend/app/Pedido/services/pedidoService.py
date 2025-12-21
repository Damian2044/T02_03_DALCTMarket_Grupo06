from app.Pedido.repositories.pedidoRepository import PedidoRepository
from app.configuracionGeneral.schemasGenerales import respuestaApi
from app.Pedido.schemas.pedidoSchemas import *
from fastapi import HTTPException
from app.Usuarios.schemas.usuarioSchemas import UsuarioPublicoSchema

class PedidoService:
    def __init__(self, dbSession):
        self.dbSession = dbSession
        self.repo = PedidoRepository(dbSession)

    def listarPedidos(self):
        pedidos = self.repo.listarPedidos()
        if not pedidos:
            return respuestaApi(success=True, message="No se encontraron pedidos", data=[])
        pedidos_schemas = [PedidoRespuestaSchema.from_orm(p) for p in pedidos]
        return respuestaApi(success=True, message="Pedidos encontrados", data=pedidos_schemas)

    def obtenerPorId(self, idPedido: int):
        pedido = self.repo.obtenerPorId(idPedido)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        pedido_schema = PedidoRespuestaSchema.from_orm(pedido)
        return respuestaApi(success=True, message="Pedido encontrado", data=pedido_schema)

    def listarPedidosPendientes(self):
        pedidos = self.repo.listarPedidosPendientes()
        if not pedidos:
            return respuestaApi(success=True, message="No se encontraron pedidos pendientes", data=[])
        pedidos_schemas = [PedidoRespuestaSchema.from_orm(p) for p in pedidos]
        return respuestaApi(success=True, message="Pedidos pendientes encontrados", data=pedidos_schemas)

    def crearPedido(self, pedidoCrear: PedidoCrearSchema, usuario: dict):
        idUsuario = usuario.get("idUsuario")
        rol = usuario.get("rol")
        resultado = self.repo.crearPedido(pedidoCrear, idUsuario, rol)
        if isinstance(resultado, dict) and resultado.get("error"):
            raise HTTPException(status_code=400, detail=resultado)
        pedido_schema = PedidoRespuestaSchema.from_orm(resultado)
        return respuestaApi(success=True, message="Pedido creado", data=pedido_schema)

    def revisarPedido(self, idPedido: int, revisar: RevisarPedidoSchema, usuario: dict):
        
        rol = usuario.get("rol")
        idUsuario = usuario.get("idUsuario")
        # Validar permisos: si el pedido fue creado por otro usuario y el rol no es Administrador, no puede aprobar/rechazar
        pedido = self.repo.obtenerPorId(idPedido)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        print(pedido.idUsuarioCreador, idUsuario, rol)
        #if pedido.idUsuarioCreador != idUsuario and rol != "Administrador":
        if rol != "Administrador":
            print(pedido.idUsuarioCreador, idUsuario, rol)
            raise HTTPException(status_code=403, detail="Solo el Administrador puede revisar pedidos creados por otros")
        if revisar.estadoPedido not in ["APROBADO", "RECHAZADO"]:
            raise HTTPException(status_code=400, detail="Estado de revisión inválido")
        resultado = self.repo.revisarPedido(idPedido, revisar.estadoPedido, revisar.observaciones, idUsuario)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        if isinstance(resultado, dict) and resultado.get("error") == "pedido_no_modificable":
            raise HTTPException(status_code=400, detail="El pedido ya fue revisado y no puede cambiar de estado")
        pedido_schema = PedidoRespuestaSchema.from_orm(resultado)
        return respuestaApi(success=True, message="Pedido revisado", data=pedido_schema)

    def listarDetallesPorPedido(self, idPedido: int):
        detalles = self.repo.listarDetallesPorPedido(idPedido)
        if not detalles:
            return respuestaApi(success=True, message="No se encontraron detalles para este pedido", data=[])
        detalles_schema = [DetallePedidoRespuestaSchema.from_orm(d) for d in detalles]
        return respuestaApi(success=True, message="Detalles encontrados", data=detalles_schema)

    def obtenerDetallePorId(self, idDetalle: int):
        detalle = self.repo.obtenerDetallePorId(idDetalle)
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        detalle_schema = DetallePedidoRespuestaSchema.from_orm(detalle)
        return respuestaApi(success=True, message="Detalle encontrado", data=detalle_schema)

    def realizarRecepcionDetalle(self, idDetalle: int, recepcion: RecepcionDetalleSchema, usuario: dict):
        rol = usuario.get("rol")
        idUsuario = usuario.get("idUsuario")
        # Permisos: solo Bodeguero y Administrador pueden realizar recepción
        if rol not in ["Bodeguero", "Administrador"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para recepcionar pedidos")
        # Solo aceptamos confirmaciones verdaderas
        if not recepcion.confirmar:
            raise HTTPException(status_code=400, detail="La recepción debe ser confirmada con {'confirmar': true}")
        resultado = self.repo.registrarRecepcionDetalle(idDetalle, recepcion.confirmar, idUsuario)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        if isinstance(resultado, dict):
            if resultado.get("error") == "ya_recibido":
                raise HTTPException(status_code=409, detail="Este detalle ya fue recepcionado previamente")
            if resultado.get("error") == "pedido_no_aprobado":
                raise HTTPException(status_code=400, detail="El pedido aún no ha sido aprobado")
            if resultado.get("error") == "confirmacion_requerida":
                raise HTTPException(status_code=400, detail="Confirmación requerida y debe ser true")
            raise HTTPException(status_code=400, detail="Error en la recepción")
        detalle_schema = DetallePedidoRespuestaSchema.from_orm(resultado)
        return respuestaApi(success=True, message="Recepción registrada", data=detalle_schema)
