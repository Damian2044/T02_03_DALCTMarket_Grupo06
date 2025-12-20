from pydantic import BaseModel

class RolSchema(BaseModel):
    idRol: int
    nombreRol: str

    class Config:
        from_attributes = True
