from app.Inventario.models.inventarioModel import Inventario
from app.Productos.models.productoModel import Producto
from sqlalchemy.orm import joinedload

class InventarioRepository:
    def __init__(self, dbSession):
        self.dbSession = dbSession

    def listarInventarios(self):
        return self.dbSession.query(Inventario).options(joinedload(Inventario.producto)).all()

    def obtenerPorId(self, idInventario: int):
        return self.dbSession.query(Inventario).options(joinedload(Inventario.producto)).filter(Inventario.idInventario == idInventario).first()

    def obtenerPorProducto(self, idProducto: int):
        return self.dbSession.query(Inventario).filter(Inventario.idProducto == idProducto).first()

    def crearInventario(self, inventario):
        # validar producto existe y está activo
        producto = self.dbSession.query(Producto).filter(Producto.idProducto == inventario.idProducto).first()
        missing = []
        if not producto:
            missing.append("producto")
        else:
            if not getattr(producto, "activoProducto", True):
                missing.append("producto_inactiva")
        if missing:
            return {"error": missing}
        datos = inventario.model_dump()
        # garantizar que cantidadMinima tenga valor si no se envía
        if datos.get("cantidadMinima") is None:
            datos["cantidadMinima"] = 0
        nuevo = Inventario(**datos)
        self.dbSession.add(nuevo)
        self.dbSession.commit()
        self.dbSession.refresh(nuevo)
        return nuevo

    def modificarInventario(self, idInventario: int, inventarioActualizar):
        inventario = self.obtenerPorId(idInventario)
        if not inventario:
            return None
        datos = inventarioActualizar.model_dump(exclude_unset=True)
        camposValidos = ["cantidadDisponible","cantidadMinima","activoInventario"]
        for campo, valor in datos.items():
            if campo in camposValidos:
                setattr(inventario, campo, valor)
        self.dbSession.commit()
        self.dbSession.refresh(inventario)
        return inventario

    def deshabilitarInventario(self, idInventario: int):
        inventario = self.obtenerPorId(idInventario)
        if not inventario:
            return None
        # Solo permitir deshabilitar si el producto asociado está deshabilitado
        producto = self.dbSession.query(Producto).filter(Producto.idProducto == inventario.idProducto).first()
        if producto and getattr(producto, "activoProducto", True):
            return False
        inventario.activoInventario = False
        self.dbSession.commit()
        self.dbSession.refresh(inventario)
        return inventario

    def crearInventariosIniciales(self):
        # Crear un inventario por cada producto existente si no tiene inventario
        productos = self.dbSession.query(Producto).all()
        for p in productos:
            existe = self.dbSession.query(Inventario).filter(Inventario.idProducto == p.idProducto).first()
            if not existe:
                nuevo = Inventario(idProducto=p.idProducto, cantidadDisponible=0, cantidadMinima=0, activoInventario=True)
                self.dbSession.add(nuevo)
        print("Inventarios por defecto creados...!")
        self.dbSession.commit()
        self.dbSession.close()
