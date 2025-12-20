from app.ParametrosSistema.repositories.parametroSistemaRepository import ParametroSistemaRepository
from app.configuracionGeneral.schemasGenerales import respuestaApi
from fastapi import HTTPException
from app.ParametrosSistema.schemas.parametroSistemaSchemas import *

class ParametroSistemaService:
    def __init__(self, dbSession):
        self.dbSession = dbSession
        # Usar nombre completo de atributo para consistencia con otros servicios
        self.parametroSistemaRepository = ParametroSistemaRepository(dbSession)

    def listarParametros(self):
        parametros = self.parametroSistemaRepository.listarParametros()
        if not parametros:
            return respuestaApi(success=True, message="No se encontraron parámetros", data=[])
        datos = [ParametroSistemaRespuestaSchema.from_orm(p) for p in parametros]
        return respuestaApi(success=True, message="Parámetros encontrados", data=datos)

    def obtenerParametroPorId(self, idParametro: int):
        parametro = self.parametroSistemaRepository.obtenerPorId(idParametro)
        if parametro is None:
            raise HTTPException(status_code=404, detail="Parámetro no encontrado")
        parametro = ParametroSistemaRespuestaSchema.from_orm(parametro)
        return respuestaApi(success=True, message="Parámetro encontrado", data=parametro)

    def crearParametro(self, parametro: ParametroSistemaCrearSchema):
        creado = self.parametroSistemaRepository.crearParametro(parametro)
        if creado is None:
            raise HTTPException(status_code=400, detail="La clave del parámetro ya existe")
        creado = ParametroSistemaRespuestaSchema.from_orm(creado)
        return respuestaApi(success=True, message="Parámetro creado", data=creado)

    def modificarParametro(self, idParametro: int, parametro: ParametroSistemaActualizarSchema):
        actualizado = self.parametroSistemaRepository.modificarParametro(idParametro, parametro)
        if actualizado is False:
            raise HTTPException(status_code=400, detail="La clave del parámetro ya existe")
        if actualizado is None:
            raise HTTPException(status_code=404, detail="Parámetro no encontrado")
        actualizado = ParametroSistemaRespuestaSchema.from_orm(actualizado)
        return respuestaApi(success=True, message="Parámetro actualizado", data=actualizado)

    def deshabilitarParametro(self, idParametro: int):
        eliminado = self.parametroSistemaRepository.deshabilitarParametro(idParametro)
        if eliminado is None:
            raise HTTPException(status_code=404, detail="Parámetro no encontrado")
        eliminado = ParametroSistemaRespuestaSchema.from_orm(eliminado)
        return respuestaApi(success=True, message="Parámetro deshabilitado", data=eliminado)

