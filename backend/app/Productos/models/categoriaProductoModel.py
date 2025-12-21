from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class CategoriaProducto(Base):
    __tablename__ = "categoriaproducto"
    idCategoriaProducto = Column(Integer, primary_key=True, autoincrement=True)
    nombreCategoria = Column(String(50), nullable=False)
    activoCategoria = Column(Boolean, default=True)
    productos = relationship("Producto", back_populates="categoria")
