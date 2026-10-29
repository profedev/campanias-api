# API REST de campañas — Render y ejecución local

API de solo lectura desarrollada con FastAPI. Devuelve el contenido completo de `campanias.json` sin modificar sus bytes, formato ni valores.

## Publicar en Render

El proyecto incluye `render.yaml` y `.python-version` para publicarlo como **Web Service** en Render. Sigue las instrucciones de [RENDER.md](RENDER.md) para conectar el repositorio y desplegarlo.

- Build Command: `python -m pip install -r requirements.txt`
- Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`

Al abrir la URL principal, `/` redirige a `/api/v1/campanias`. Los pasos siguientes permiten seguir ejecutando la misma API localmente.

## Requisitos

- Python 3.10 o posterior con `pip`; el proyecto se verificó con Python 3.12.
- Una terminal: PowerShell en Windows o una terminal en macOS/Linux.
- Conexión a Internet para instalar las dependencias por primera vez.

No requiere base de datos, cuenta de Azure ni variables de entorno.

## 1. Preparar la carpeta

Si recibiste el proyecto como ZIP, extráelo antes de continuar. Abre una terminal en la carpeta que contiene estos archivos:

```text
campanias-api/
├── main.py
├── campanias.json
├── requirements.txt
├── requirements-dev.txt
├── test_api.py
└── README.md
```

Mantén `campanias.json` junto a `main.py`. Ejecuta los comandos siguientes desde esa carpeta.

## 2. Instalar y ejecutar en Windows

En PowerShell, comprueba que Python esté disponible:

```powershell
python --version
```

Crea un entorno virtual e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Inicia la API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Mantén la terminal abierta mientras usas la API. Estos comandos usan directamente el Python del entorno virtual; no es necesario activarlo ni cambiar la política de ejecución de PowerShell.

Si `python` no se reconoce o abre Microsoft Store, instala Python y vuelve a abrir la terminal. Si tienes el lanzador de Windows, puedes usar `py -3 --version` y `py -3 -m venv .venv` para los dos comandos iniciales.

## 3. Instalar y ejecutar en macOS o Linux

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Si el sistema indica que falta el módulo `venv`, instala el paquete de entornos virtuales correspondiente a tu distribución y versión de Python, y vuelve a crear el entorno.

## 4. Comprobar la API

Con el servidor encendido, abre estas direcciones en el navegador:

| Dirección | Resultado esperado |
| --- | --- |
| http://127.0.0.1:8000/api/v1/campanias | Documento JSON original completo, HTTP 200 y `Content-Type: application/json` |
| http://127.0.0.1:8000/health | HTTP 200 y `{"status":"ok"}` |
| http://127.0.0.1:8000/docs | Documentación interactiva para probar los endpoints |

También puedes consultar la API desde una segunda terminal de PowerShell:

```powershell
curl.exe -i http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/api/v1/campanias
```

En macOS/Linux usa `curl` en lugar de `curl.exe`.

La dirección raíz `http://127.0.0.1:8000/` redirige a `/api/v1/campanias`. Para comprobar el estado del servicio usa `/health`.

## Detener, reiniciar y desarrollar

Para detener la API, presiona **Ctrl+C** en la terminal del servidor. Para volver a iniciarla, ejecuta otra vez el comando de Uvicorn; no necesitas reinstalar las dependencias.

Durante el desarrollo puedes activar la recarga automática del código Python:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

En macOS/Linux sustituye `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

El servidor escucha en `127.0.0.1`, por lo que se accede desde el mismo equipo. Si el puerto 8000 está ocupado, usa `--port 8001` y cambia el puerto en las URLs de consulta.

## Pruebas automatizadas

Las pruebas no requieren tener el servidor de Uvicorn encendido.

En Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest -v
```

En macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest -v
```

El resultado esperado es **4 pruebas aprobadas** y el mensaje `OK`. Comprueban la redirección de la raíz, la integridad del archivo original, la igualdad byte por byte de la respuesta, el tipo de contenido, el endpoint de salud y el rechazo de POST, PUT, PATCH y DELETE.

## Conservación del JSON original

`campanias.json` contiene 3980 bytes. La aplicación lo lee y valida al arrancar, y devuelve esos mismos bytes en cada consulta. Conserva espacios, saltos de línea, acentos, orden de las claves, números y fechas, sin agregar campos ni aplicar filtros o paginación.

El archivo se mantiene en memoria durante la ejecución. Si falta o contiene JSON inválido, la aplicación no arranca. La recarga de código Python no debe usarse para actualizar este archivo: cualquier sustitución deliberada requiere reiniciar el servidor. Para conservar el contrato de esta API, mantén el adjunto original sin cambios.

SHA-256 original:

```text
9f1b5c1f890356cd3ff824e801119bfa853bd6c7f1ff107fa7372608da2855d3
```

Puedes comprobarlo en PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\campanias.json
```

## Solución de problemas

| Problema | Acción |
| --- | --- |
| `No module named uvicorn` o `fastapi` | Instala `requirements.txt` con el Python de `.venv` y usa ese mismo ejecutable para arrancar. |
| `Could not import module "main"` | Abre la terminal en la carpeta que contiene `main.py`. |
| No se encuentra `campanias.json` | Coloca el archivo original junto a `main.py`. |
| Puerto ocupado / `Address already in use` | Detén el proceso anterior o inicia con `--port 8001`. |
| El navegador no puede conectarse | Comprueba que la terminal del servidor siga abierta y que la URL use el puerto elegido. |
| Error 404 al abrir `/` | Comprueba que estés ejecutando esta versión de `main.py` y reinicia el servidor; la raíz ahora redirige a campañas. |
| Falla la prueba de integridad | Restaura `campanias.json` desde el adjunto original; no cambies la huella esperada para ocultar la diferencia. |

## Dependencias y archivos

Las dependencias de ejecución están fijadas en `requirements.txt`: FastAPI 0.162.0 y Uvicorn 0.54.0. `requirements-dev.txt` agrega HTTPX para las pruebas.

| Archivo | Función |
| --- | --- |
| `main.py` | Define la API y sus endpoints. |
| `campanias.json` | Documento original servido sin cambios. |
| `requirements.txt` | Dependencias para ejecutar la API. |
| `requirements-dev.txt` | Dependencias para ejecutar las pruebas. |
| `test_api.py` | Pruebas del comportamiento y la integridad del JSON. |
