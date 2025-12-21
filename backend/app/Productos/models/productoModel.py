from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Producto(Base):
    __tablename__ = "producto"
    idProducto = Column(Integer, primary_key=True, autoincrement=True)
    idCategoriaProducto = Column(Integer, ForeignKey("categoriaproducto.idCategoriaProducto"), nullable=False)
    idProveedor = Column(Integer, ForeignKey("proveedor.idProveedor"), nullable=False)
    nombreProducto = Column(String(100), nullable=False)
    descripcionProducto = Column(String(255), nullable=True)
    precioUnitarioVenta = Column(Float, nullable=False)
    precioUnitarioCompra = Column(Float, nullable=False)
    tieneIva = Column(Boolean, default=True, nullable=False)
    activoProducto = Column(Boolean, default=True, nullable=False)

    categoria = relationship("CategoriaProducto", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    inventario = relationship("Inventario", back_populates="producto")
    detallesPedido = relationship("DetallePedido", back_populates="producto")
    promociones = relationship("Promocion", back_populates="producto")
    detallesVenta = relationship("DetalleVenta", back_populates="producto")
