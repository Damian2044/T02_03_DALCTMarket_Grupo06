from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class CajaHistorial(Base):
    __tablename__ = "cajahistorial"
    idCaja = Column(Integer, primary_key=True, autoincrement=True)
    idUsuarioCaja = Column(Integer, ForeignKey("usuario.idUsuario"), nullable=False)
    fechaAperturaCaja = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fechaCierreCaja = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    montoInicialDeclarado = Column(Float, nullable=False)
    montoCierreDeclarado = Column(Float, nullable=True)
    montoCierreSistema = Column(Float, nullable=True)
    diferenciaCaja = Column(Float, nullable=True)
    estadoCaja = Column(String(20), nullable=False, default="ABIERTA")
    detalle = Column(String(500), nullable=True)

    usuario = relationship("Usuario", back_populates="cajas")