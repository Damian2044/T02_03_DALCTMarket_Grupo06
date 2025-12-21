from fastapi import APIRouter, Depends
from app.Inventario.services.inventarioService import InventarioService
from app.Inventario.schemas.inventarioSchemas import *
from app.database import obtenerSesion
from app.configuracionGeneral.seguridadJWT import protegerRuta
from app.configuracionGeneral.schemasGenerales import respuestaApi

router = APIRouter()

@router.get("/", tags=["Inventario"], summary="Obtener todos los inventarios", status_code=200, response_model=respuestaApi)
async def obtenerTodosLosInventarios(dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "GET"))):
    return InventarioService(dbSession).listarInventarios()

@router.get("/{idInventario}", tags=["Inventario"], summary="Obtener un inventario por id", status_code=200, response_model=respuestaApi)
async def obtenerInventarioPorId(idInventario: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "GET"))):
    return InventarioService(dbSession).obtenerPorId(idInventario)

@router.get("/producto/{idProducto}", tags=["Inventario"], summary="Obtener inventario por id de producto", status_code=200, response_model=respuestaApi)
async def obtenerInventarioPorProducto(idProducto: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "GET"))):
    return InventarioService(dbSession).obtenerPorProducto(idProducto)

@router.post("/", tags=["Inventario"], description="Crear un nuevo inventario para un producto existente", response_model=respuestaApi)
async def crearInventario(inventario: InventarioCrearSchema, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "POST"))):
    result, status = InventarioService(dbSession).crearInventario(inventario)
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=status, content=result.model_dump())

@router.put("/{idInventario}", tags=["Inventario"], summary="Actualizar un inventario por id", description="Administrador: puede modificar `cantidadDisponible`, `cantidadMinima` y `activoInventario`. Bodeguero: puede modificar `cantidadMinima` y `activoInventario` (no puede cambiar `cantidadDisponible`).", status_code=200, response_model=respuestaApi)
async def actualizarInventario(idInventario: int, inventario: InventarioActualizarSchema, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "PUT"))):
    return InventarioService(dbSession).modificarInventario(idInventario, inventario, usuario)

@router.delete("/{idInventario}", tags=["Inventario"], summary="Deshabilitar un inventario por id", status_code=200, response_model=respuestaApi)
async def deshabilitarInventario(idInventario: int, dbSession=Depends(obtenerSesion), usuario=Depends(protegerRuta("Inventario", "DELETE"))):
    return InventarioService(dbSession).deshabilitarInventario(idInventario)
