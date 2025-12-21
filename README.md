# SGM-DALCT Backend
Repositorio del backend del Sistema de Gestión de Minimercado DALCT Market (SGM-DALCT) para la tarea de Ingeniería de Software 02.03.
Incluye funcionalidades de usuarios, roles, productos, inventario, proveedores, ventas, caja y reportes.
# SGM-DALCT (Tarea 02.03)-Documentación del Backend

## 1. Introducción
Este documento describe la arquitectura, tecnologías, módulos y organización del código del backend del Sistema de Gestión de Minimercado DALCT Market (SGM-DALCT), desarrollado como parte de la tarea 02.03 de Ingeniería de Software. El backend está implementado utilizando **FastAPI** con **Python 3.12+** y utiliza **PostgreSQL 17** como base de datos, todo ello contenido en **Docker** para facilitar su despliegue y ejecución.
---

## 2. Tecnologías y herramientas utilizadas
- Lenguaje de programación: **Python 3.12+**
- Framework Web: **FastAPI** (documentación automática y rapidez para APIs REST)
- Gestión de datos: **SQLAlchemy** + **Pydantic**
- Base de datos: **PostgreSQL 17**
- Contenerización: **Docker**
- Documentación/Interfaz: **Swagger** (endpoints en `/docs`)

---

## 3. Arquitectura del código
El backend está estructurado siguiendo un esquema modular basado en modelo/repositorio/servicio/controlador:
- **Modelo:** Entidades y relaciones (Usuario, Producto, Inventario, Venta, Cliente, Caja, Pedido, etc.).
- **Repositorio:** Interacción con la base de datos (CRUD, consultas especializadas).
- **Servicio:** Lógica de negocio (cálculo de totales, validaciones, aplicación de promociones, apertura/cierre de caja, etc.).
- **Controlador / Router:** Endpoints REST que consumen los servicios y validan entradas.

Cada módulo funcional está agrupado en su propia carpeta con subcarpetas `models`, `repositories`, `services` y `controllers` según corresponda, lo que facilita la división del trabajo y el mantenimiento.

---

## 4. Módulos del sistema (Resumen)
1. **Módulo ParametrosSistema**
   - Función: Gestionar parámetros configurables (IVA, nombreNegocio, direccionNegocio, telefonoNegocio, correoNegocio, logoNegocio).
   - Entidades: `ParametroSistema`.

2. **Módulo Usuarios**
   - Función: Gestión de usuarios y roles, autenticación y autorización.
   - Entidades: `Usuario`, `Rol`.

3. **Módulo Productos**
   - Función: Gestión de productos, categorías.
   - Entidades: `Producto`, `CategoriaProducto`, `Proveedor`.

4. **Módulo Inventario**
   - Función: Control de existencias, cantidades mínimas y actualización automática tras ventas/pedidos.
   - Entidades: `Inventario`.

5. **Módulo Pedidos**
   - Función: Registro, aprobación y recepción de pedidos para nuevos ingresos.
   - Entidades: `Pedido`, `DetallePedido`

6. **Módulo Ventas**
   - Función: Registro de ventas, cálculo de totales, aplicación de descuentos y generación de comprobantes.
   - Entidades: `Venta`, `DetalleVenta`, `Promocion`.

7. **Módulo Clientes**
   - Función: Gestión de clientes y seguimiento de compras.
   - Entidades: `Cliente`.

8. **Módulo Caja**
   - Función: Apertura, cierre y cuadre de caja; control de efectivo y métodos de pago.
   - Entidades: `CajaHistorial`.

9. **Módulo Reportes**
   - Función: Generación de reportes agregados a partir de datos de los módulos anteriores.

---

## 5. Organización de carpetas (recomendación)
Estructura por módulo (mínimo recomendado):
```
<modulo>/
  models/
  repositories/
  services/
  controllers/
  schemas/
```

---

## 6. Repositorio de Código
- **Enlace:** (poner enlace aquí)

### 6.1 Clonación y uso
1. Clonar y acceder al backend:
```bash
git clone https://github.com/Damian2044/T02_03_DALCTMarket_Grupo06.git
cd T02_03_DALCTMarket_Grupo06
```
2. Ejecutar con Docker Compose (recomendado):
```bash
docker compose up --build
# o en segundo plano:
# docker compose up -d --build
```
También puede ejecutarse localmente pero se debe crear y configurar la base de datos PostgreSQL manualmente:
1. Instalar dependencias:
```bash
pip install -r requerimientos.txt
```
2. Inicar el proyecto:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
4. La documentación interactiva estará disponible en:

- Local: http://localhost:8000/docs
- Deploy: https://t02-03-dalctmarket-grupo06.onrender.com/docs

---

## 7. Distribución de tareas por integrante
| Integrante | Tareas |
|---|---|
| Damian Barahona | Configuración inicial de FastAPI, Pydantic y SQLAlchemy. Desarrollo completo de `ParametrosSistema` y `Usuario`.
| Kenin Cayambe | Desarrollo completo de  `Clientes`(models, repositories, services, controllers).
| Sthalin Chasipanta | Desarrollo completo de `Pedidos` y `Venta` (models, repositories, services, controllers).
| Cristian Licto | Desarrollo completo de `Productos` e `Inventario` (models, repositories, services, controllers).
| Juan Tandazo | Desarrollo completo de `Caja` y `Reportes` (services y controllers, consumo de datos de otros módulos).

---

## 8. Usuarios por defecto (pruebas)
- Se incluyen **usuarios por defecto** para facilitar pruebas. **Acceso:** identificación mediante **cédula** (`cedulaUsuario`).
**Tabla de usuarios por defecto**

| Usuario | Cédula (login) | Rol |
|---|---|---|
| admin | `admin` | Administrador |
| bodeguero | `bodeguero` | Bodeguero |
| cajero | `cajero` | Cajero |

todos con la password de 1234.
