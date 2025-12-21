from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from app.Productos.schemas.productoSchemas import ProductoRespuestaSchema
from app.Usuarios.schemas.usuarioSchemas import UsuarioPublicoSchema

class DetallePedidoCrearSchema(BaseModel):
    idProducto: int = Field(..., example=1)
    cantidadSolicitada: int = Field(..., example=10, ge=1)

class PedidoCrearSchema(BaseModel):
    detalles: List[DetallePedidoCrearSchema]

    model_config = {
        "json_schema_extra": {
            "example": {
                "detalles": [
                    {"idProducto": 1, "cantidadSolicitada": 10},
                    {"idProducto": 2, "cantidadSolicitada": 5}
                ]
            }
        }
    }
class DetallePedidoRespuestaSchema(BaseModel):
    idDetallePedido: int
    idPedido: int
    cantidadSolicitada: int
    precioUnitarioCompra: float
    estadoDetalle: str
    fechaRecepcion: Optional[datetime] = Field(None, example="2025-12-20T15:30:00Z")
    producto: Optional[ProductoRespuestaSchema] = None
    usuarioReceptor: Optional[UsuarioPublicoSchema] = None

    class Config:
        from_attributes = True

class PedidoRespuestaSchema(BaseModel):
    idPedido: int
    usuarioCreador: UsuarioPublicoSchema
    usuarioAprobador: Optional[UsuarioPublicoSchema] = None
    totalCostoPedido: float
    fechaCreacion: Optional[datetime] = Field(None, example="2025-12-20T15:30:00Z")
    estadoPedido: str
    observaciones: Optional[str] = None
    detalles: List[DetallePedidoRespuestaSchema] = []

    class Config:
        from_attributes = True

class RevisarPedidoSchema(BaseModel):
    estadoPedido: Literal["APROBADO","RECHAZADO"] = Field(..., example="APROBADO", description="Enviar 'APROBADO' o 'RECHAZADO'. Solo Administrador puede aprobar pedidos creados por otros.")
    observaciones: Optional[str] = None

class RecepcionDetalleSchema(BaseModel):
    confirmar: bool = Field(..., example=True, description="Debe ser true para confirmar la recepción completa del detalle")

