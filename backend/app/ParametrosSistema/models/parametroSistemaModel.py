from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class ParametroSistema(Base):
    __tablename__ = "parametrosistema"
    idParametroSistema = Column(Integer, primary_key=True, autoincrement=True)
    claveParametro = Column(String(50), nullable=False)
    valorParametro = Column(String(500), nullable=False)
    activoParametro = Column(Boolean, default=True)
