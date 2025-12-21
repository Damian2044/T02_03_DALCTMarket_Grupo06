from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Proveedor(Base):
    __tablename__ = "proveedor"
    idProveedor = Column(Integer, primary_key=True, autoincrement=True)
    razonSocial = Column(String(100), nullable=False)
    ruc = Column(String(13), nullable=False, unique=True)
    direccionProveedor = Column(String(100), nullable=False)
    telefonoProveedor = Column(String(20), nullable=False)
    emailProveedor = Column(String(100), nullable=False)
    activoProveedor = Column(Boolean, default=True)
    productos = relationship("Producto", back_populates="proveedor")
