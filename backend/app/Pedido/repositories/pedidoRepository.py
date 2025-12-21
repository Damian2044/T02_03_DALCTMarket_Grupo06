from app.Pedido.models.pedidoModel import Pedido
from app.Pedido.models.detallePedidoModel import DetallePedido
from app.Productos.models.productoModel import Producto
from app.Inventario.models.inventarioModel import Inventario
from sqlalchemy.orm import joinedload, selectinload
from typing import List
from datetime import datetime, timezone, timedelta

class PedidoRepository:
    def __init__(self, dbSession):
        self.dbSession = dbSession

    def listarPedidos(self) -> List[Pedido]:
        # Use selectinload for 1-N relationships to avoid JOIN + LIMIT issues
        return (self.dbSession.query(Pedido)
                .options(
                    joinedload(Pedido.usuarioCreador),
                    joinedload(Pedido.usuarioAprobador),
                    selectinload(Pedido.detalles).selectinload(DetallePedido.producto),
                    selectinload(Pedido.detalles).selectinload(DetallePedido.usuarioReceptor)
                )
                .all())

    def obtenerPorId(self, idPedido: int):
        # Evitar usar joinedload en colecciones si luego se aplica limit/first; usamos selectinload para 1-N
        return (self.dbSession.query(Pedido)
                .options(
                    joinedload(Pedido.usuarioCreador),
                    joinedload(Pedido.usuarioAprobador),
                    selectinload(Pedido.detalles).selectinload(DetallePedido.producto),
                    selectinload(Pedido.detalles).selectinload(DetallePedido.usuarioReceptor)
                )
                .filter(Pedido.idPedido == idPedido).first())

    def listarPedidosPendientes(self) -> List[Pedido]:
        return self.dbSession.query(Pedido).filter(Pedido.estadoPedido == "PENDIENTE_REVISION").all()

    def crearPedido(self, pedidoCrear, idUsuarioCreador: int, rolUsuario: str):
        # Validar productos y calcular total
        total = 0.0
        detalles_objs = []
        missing = []
        for d in pedidoCrear.detalles:
            producto = self.dbSession.query(Producto).filter(Producto.idProducto == d.idProducto).first()
            if not producto:
                missing.append({"idProducto": d.idProducto, "error": "producto_no_encontrado"})
                continue
            # No permitir pedidos de productos inactivos
            if not producto.activoProducto:
                missing.append({"idProducto": d.idProducto, "error": "producto_inactivo"})
                continue
            # El precio se toma del producto registrado; el payload solo provee id y cantidad
            precio = producto.precioUnitarioCompra
            total += precio * d.cantidadSolicitada
            detalle = DetallePedido(
                idProducto=d.idProducto,
                cantidadSolicitada=d.cantidadSolicitada,
                precioUnitarioCompra=precio,
                # El detalle inicia siempre en PENDIENTE_REVISION; la aprobación de detalles ocurre en la revisión del pedido
                estadoDetalle="PENDIENTE_REVISION"
            )
            detalles_objs.append(detalle)
        if missing:
            return {"error": missing}
        # Si el creador es Administrador, el pedido se aprueba automáticamente y el mismo usuario es el aprobador
        estado_inicial = "PENDIENTE_REVISION"
        idUsuarioAprobador = None
        if rolUsuario == "Administrador":
            estado_inicial = "APROBADO"
            idUsuarioAprobador = idUsuarioCreador
            # Si se aprueba automáticamente, actualizar los detalles a PENDIENTE_RECEPCION
            for d in detalles_objs:
                if d.estadoDetalle == "PENDIENTE_REVISION":
                    d.estadoDetalle = "PENDIENTE_RECEPCION"
        quitoTZ = timezone(timedelta(hours=-5))
        nuevo = Pedido(
            idUsuarioCreador=idUsuarioCreador,
            idUsuarioAprobador=idUsuarioAprobador,
            totalCostoPedido=total,
            fechaCreacion=datetime.now(quitoTZ),
            estadoPedido=estado_inicial,
            observaciones=None
        )
        self.dbSession.add(nuevo)
        self.dbSession.flush()
        for det in detalles_objs:
            det.idPedido = nuevo.idPedido
            self.dbSession.add(det)
        self.dbSession.commit()
        self.dbSession.refresh(nuevo)
        return nuevo

    def revisarPedido(self, idPedido: int, estadoNuevo: str, observaciones: str, idUsuarioAprobador: int):
        pedido = self.dbSession.query(Pedido).filter(Pedido.idPedido == idPedido).first()
        if not pedido:
            return None
        # No permitir cambios si el pedido ya fue revisado (no está en pendiente)
        if pedido.estadoPedido != "PENDIENTE_REVISION":
            return {"error": "pedido_no_modificable"}
        pedido.estadoPedido = estadoNuevo
        pedido.observaciones = observaciones
        pedido.idUsuarioAprobador = idUsuarioAprobador
        # Si se aprueba, pasar detalles a PENDIENTE_RECEPCION
        if estadoNuevo == "APROBADO":
            for d in pedido.detalles:
                if d.estadoDetalle == "PENDIENTE_REVISION":
                    d.estadoDetalle = "PENDIENTE_RECEPCION"
        # Si se rechaza, marcar detalles como NO_APROBADO
        if estadoNuevo == "RECHAZADO":
            for d in pedido.detalles:
                d.estadoDetalle = "NO_APROBADO"
        self.dbSession.commit()
        self.dbSession.refresh(pedido)
        return pedido

    def listarDetallesPorPedido(self, idPedido: int):
        return self.dbSession.query(DetallePedido).options(joinedload(DetallePedido.producto)).filter(DetallePedido.idPedido == idPedido).all()

    def obtenerDetallePorId(self, idDetalle: int):
        return self.dbSession.query(DetallePedido).options(joinedload(DetallePedido.producto)).filter(DetallePedido.idDetallePedido == idDetalle).first()

    def registrarRecepcionDetalle(self, idDetalle: int, confirmar: bool, idUsuarioReceptor: int):
        # Solo procede si confirmar == True
        detalle = self.dbSession.query(DetallePedido).filter(DetallePedido.idDetallePedido == idDetalle).first()
        if not detalle:
            return None
        # No permitir recepción si el pedido no está aprobado (sigue pendiente)
        pedido = self.dbSession.query(Pedido).filter(Pedido.idPedido == detalle.idPedido).first()
        if pedido is None:
            return None
        if pedido.estadoPedido == "PENDIENTE_REVISION":
            return {"error": "pedido_no_aprobado"}
        if not confirmar:
            # No permitimos confirmaciones falsas
            return {"error": "confirmacion_requerida"}
        # Si ya está recibido, no permitimos doble recepción
        if detalle.estadoDetalle == "RECIBIDO":
            return {"error": "ya_recibido"}
        # Registrar quién recibió y cuándo
        detalle.idUsuarioReceptor = idUsuarioReceptor
        quitoTZ = timezone(timedelta(hours=-5))
        detalle.fechaRecepcion = datetime.now(quitoTZ)
        # Marcar el detalle como recibido (se asume recepción completa del detalle)
        detalle.estadoDetalle = "RECIBIDO"
        # Actualizar inventario con la cantidad solicitada (recepción completa)
        inventario = self.dbSession.query(Inventario).filter(Inventario.idProducto == detalle.idProducto).first()
        if inventario:
            inventario.cantidadDisponible = (inventario.cantidadDisponible or 0) + detalle.cantidadSolicitada
        else:
            # Crear registro de inventario si no existe
            nuevo_inv = Inventario(
                idProducto=detalle.idProducto,
                cantidadDisponible=detalle.cantidadSolicitada,
                cantidadMinima=0,
                activoInventario=True
            )
            self.dbSession.add(nuevo_inv)
        self.dbSession.commit()
        self.dbSession.refresh(detalle)
        # Actualizar estado del pedido según estados de sus detalles
        detalles = self.dbSession.query(DetallePedido).filter(DetallePedido.idPedido == pedido.idPedido).all()
        todos_recibidos = all(d.estadoDetalle == "RECIBIDO" for d in detalles)
        alguno_recibido = any(d.estadoDetalle == "RECIBIDO" for d in detalles)
        if todos_recibidos:
            pedido.estadoPedido = "COMPLETAMENTE_RECIBIDO"
        elif alguno_recibido:
            pedido.estadoPedido = "PARCIALMENTE_RECIBIDO"
        self.dbSession.commit()
        self.dbSession.refresh(pedido)
        return detalle

    def crearPedidosIniciales(self):
        """Crear pedidos de ejemplo para facilitar pruebas automáticas/manuales.
        - Un pedido creado por el Admin (idUsuario=1) que debe quedar APROBADO automáticamente.
        - Un pedido creado por el Bodeguero (idUsuario=2) que debe quedar PENDIENTE_REVISION.
        Usa como productos de prueba 'Cola 2 Litros' y 'Jugo de Naranja 1L' si existen.
        """
        # No duplicar si ya hay pedidos
        existe = self.dbSession.query(Pedido).first()
        if existe:
            return
        # Buscar productos de prueba
        producto1 = self.dbSession.query(Producto).filter(Producto.nombreProducto == "Cola 2 Litros").first()
        producto2 = self.dbSession.query(Producto).filter(Producto.nombreProducto == "Jugo de Naranja 1L").first()
        if not producto1 or not producto2:
            # No crear si faltan productos base
            return
        # Construir schemas de detalle/pedido
        try:
            from app.Pedido.schemas.pedidoSchemas import PedidoCrearSchema, DetallePedidoCrearSchema
            admin_pedido = PedidoCrearSchema(detalles=[DetallePedidoCrearSchema(idProducto=producto1.idProducto, cantidadSolicitada=5), DetallePedidoCrearSchema(idProducto=producto2.idProducto, cantidadSolicitada=3)])
            bodeguero_pedido = PedidoCrearSchema(detalles=[DetallePedidoCrearSchema(idProducto=producto1.idProducto, cantidadSolicitada=2)])
            # Crear usando la lógica existente (admin será aprobado automáticamente)
            self.crearPedido(admin_pedido, 1, "Administrador")
            self.crearPedido(bodeguero_pedido, 2, "Bodeguero")
        except Exception:
            # Si por alguna razón no se pueden crear los pedidos, no romper el startup
            return
