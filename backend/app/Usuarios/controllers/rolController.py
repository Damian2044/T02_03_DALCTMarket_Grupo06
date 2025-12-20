from fastapi import APIRouter,Depends
from app.Usuarios.services.rolService import RolService
from app.database import obtenerSesion
from app.configuracionGeneral.schemasGenerales import respuestaApi

router = APIRouter()

@router.get("/", tags=["Roles"],
            summary="Obtener todos los roles",
            status_code=200,
            response_model=respuestaApi)
async def obtenerTodosLosRoles(dbSession=Depends(obtenerSesion)):
    rolService = RolService(dbSession)
    return rolService.obtenerTodos()

@router.get("/{idRol}", tags=["Roles"],
            summary="Obtener un rol por id",
            status_code=200,
            response_model=respuestaApi)
async def obtenerRolPorId(idRol: int, dbSession=Depends(obtenerSesion)):
    rolService = RolService(dbSession)
    return rolService.obtenerPorId(idRol)

@router.get("/nombre/{nombreRol}", tags=["Roles"],
            summary="Obtener un rol por nombre",
            status_code=200,
            response_model=respuestaApi)
async def obtenerRolPorNombre(nombreRol: str, dbSession=Depends(obtenerSesion)):
    rolService = RolService(dbSession)
    return rolService.obtenerPorNombre(nombreRol)
