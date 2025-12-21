from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DetallePedido(Base):
    __tablename__ = "detallepedido"
    idDetallePedido = Column(Integer, primary_key=True, autoincrement=True)
    idPedido = Column(Integer, ForeignKey("pedido.idPedido"), nullable=False)
    idProducto = Column(Integer, ForeignKey("producto.idProducto"), nullable=False)
    idUsuarioReceptor = Column(Integer, ForeignKey("usuario.idUsuario"), nullable=True)
    cantidadSolicitada = Column(Integer, nullable=False)
    precioUnitarioCompra = Column(Float, nullable=False)
    estadoDetalle = Column(String(30), nullable=False)
    fechaRecepcion = Column(DateTime, nullable=True)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detallesPedido")
    usuarioReceptor = relationship("Usuario", foreign_keys=[idUsuarioReceptor])
