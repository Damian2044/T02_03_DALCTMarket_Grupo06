from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Promocion(Base):
    __tablename__ = "promocion"
    idPromocion = Column(Integer, primary_key=True, autoincrement=True)
    idProducto = Column(Integer, ForeignKey("producto.idProducto"), nullable=False)
    nombrePromocion = Column(String(100), nullable=False)
    porcentajePromocion = Column(Float, nullable=False)
    fechaInicioPromocion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fechaFinPromocion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    activoPromocion = Column(Boolean, default=True, nullable=False)

    producto = relationship("Producto", back_populates="promociones")
    detallesVenta = relationship("DetalleVenta", back_populates="promocion")
