from fastapi import HTTPException
from app.configuracionGeneral.schemasGenerales import respuestaApi
from app.Usuarios.repositories.rolRepository import RolRepository
from app.Usuarios.schemas.rolSchemas import RolSchema
class RolService:
    def __init__(self, dbSession):
        self.dbSession = dbSession
        self.rolRepository = RolRepository(dbSession)
    
    def obtenerTodos(self):
        roles=self.rolRepository.obtenerTodos()
        if not roles:
            return respuestaApi(success=True, message="No se encontraron roles", data=[])
        roles=[RolSchema.from_orm(rol) for rol in roles]
        return respuestaApi(success=True, message="Roles encontrados", data=roles)

    def obtenerPorId(self, idRol: int):
        rol=self.rolRepository.obtenerPorId(idRol)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        rol=RolSchema.from_orm(rol)
        return respuestaApi(success=True, message="Rol encontrado", data=rol)
    
    def obtenerPorNombre(self, nombreRol: str):
        rol=self.rolRepository.obtenerPorNombre(nombreRol)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        rol=RolSchema.from_orm(rol)
        return respuestaApi(success=True, message="Rol encontrado", data=rol)
    


    


    