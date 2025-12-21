from pydantic import BaseModel, Field
from typing import Optional
from app.Productos.schemas.productoSchemas import ProductoRespuestaSchema

class InventarioCrearSchema(BaseModel):
    idProducto: int = Field(..., example=1)
    cantidadDisponible: int = Field(..., example=10)
    cantidadMinima: Optional[int] = Field(0, example=0)

class InventarioActualizarSchema(BaseModel):
    cantidadDisponible: Optional[int] = Field(None, example=20)
    cantidadMinima: Optional[int] = Field(None, example=5)
    activoInventario: Optional[bool] = Field(None, example=True)

class InventarioRespuestaSchema(BaseModel):
    idInventario: int
    cantidadDisponible: int
    cantidadMinima: int
    activoInventario: bool
    producto: ProductoRespuestaSchema

    class Config:
         from_attributes = True
