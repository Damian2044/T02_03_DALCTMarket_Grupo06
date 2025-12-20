from app.Usuarios.models.rolModel import Rol

class RolRepository:
    def __init__(self, dbSession):
        self.dbSession = dbSession

    def obtenerPorId(self, idRol: int):
        return self.dbSession.query(Rol).filter(Rol.idRol == idRol).first()
    
    def obtenerTodos(self):
        return self.dbSession.query(Rol).all()
    
    def obtenerPorNombre(self, nombreRol: str):
        return self.dbSession.query(Rol).filter(Rol.nombreRol == nombreRol).first()
    
    def crearRolesPorDefecto(self):
        ROLES_POR_DEFECTO = ["Administrador", "Bodeguero", "Cajero"]
        for rol in ROLES_POR_DEFECTO:
            if not self.obtenerPorNombre(rol):
                self.dbSession.add(Rol(nombreRol=rol))          
        self.dbSession.commit()
        self.dbSession.close()
        print("Roles por defecto creados...!")
    

    
