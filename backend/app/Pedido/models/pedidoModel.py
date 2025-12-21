from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedido"
    idPedido = Column(Integer, primary_key=True, autoincrement=True)
    idUsuarioCreador = Column(Integer, ForeignKey("usuario.idUsuario"), nullable=False)
    idUsuarioAprobador = Column(Integer, ForeignKey("usuario.idUsuario"), nullable=True)
    totalCostoPedido = Column(Float, nullable=False, default=0.0)
    fechaCreacion = Column(DateTime(timezone=True), server_default=func.now())
    estadoPedido = Column(String(30), nullable=False)
    observaciones = Column(String(500), nullable=True)

    detalles = relationship("DetallePedido", back_populates="pedido")

    # Relaciones a usuarios para incluir información completa en respuestas
    #usuarioCreador = relationship("Usuario", foreign_keys=[idUsuarioCreador])
    #usuarioAprobador = relationship("Usuario", foreign_keys=[idUsuarioAprobador])
    usuarioCreador = relationship(
        "Usuario",
        foreign_keys=[idUsuarioCreador],
        back_populates="pedidosCreados"
    )

    usuarioAprobador = relationship(
        "Usuario",
        foreign_keys=[idUsuarioAprobador],
        back_populates="pedidosAprobados"
    )
