# Publicar la API en Render

El proyecto está preparado para un Web Service de Python en Render. No requiere Docker, base de datos ni disco persistente. El JSON original se incluye con el código y se sirve sin cambios.

## 1. Subir el proyecto a un repositorio

Extrae `campanias-api-render.zip` y sube su contenido a un repositorio GitHub, GitLab o Bitbucket al que Render pueda acceder. Render desplegará desde ese repositorio; el ZIP entregado sirve para trasladar los archivos, no se carga directamente como servicio.

Coloca estos archivos en la raíz del repositorio, sin una carpeta contenedora adicional:

```text
main.py
campanias.json
requirements.txt
requirements-dev.txt
test_api.py
render.yaml
.python-version
.gitattributes
.gitignore
README.md
RENDER.md
```

Incluye los archivos que empiezan por punto. `.python-version` fija Python 3.12.14 y `.gitattributes` evita que Git transforme los saltos de línea de `campanias.json`. No subas `.venv`, archivos `.env` ni credenciales.

## 2. Desplegar con la configuración incluida

1. Entra a [Render Dashboard](https://dashboard.render.com/).
2. Selecciona **New > Blueprint** y conecta el repositorio.
3. Selecciona la rama que contiene los archivos y utiliza `render.yaml` como Blueprint.
4. Revisa el nombre del servicio, la región y el plan antes de crearlo. El archivo propone `campanias-api` y plan `free`; puedes cambiar el nombre en `render.yaml` antes de desplegar.
5. Aplica la configuración y espera a que finalice el despliegue. Revisa los logs si falla.

El Blueprint configura instalación de dependencias, comando de inicio, Health Check y despliegues automáticos cuando subes cambios a la rama conectada. La referencia oficial de estos campos está en [Render Blueprints](https://render.com/docs/blueprint-spec).

El plan gratuito está pensado para pruebas: se suspende después de 15 minutos sin tráfico y la siguiente solicitud puede tardar alrededor de un minuto en activarlo. Para disponibilidad continua, selecciona un plan de pago. Consulta las [limitaciones oficiales del plan gratuito](https://render.com/docs/free).

## Alternativa: configuración manual o servicio existente

Si ya creaste el servicio, actualiza estos valores en **Settings** y publica el último commit. Si es nuevo, selecciona **New > Web Service**, conecta el repositorio y configura:

| Campo | Valor |
| --- | --- |
| Language / Runtime | Python 3 |
| Root Directory | Vacío, si los archivos están en la raíz del repositorio |
| Build Command | `python -m pip install -r requirements.txt` |
| Start Command | `python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |
| Python | 3.12.14, definido por `.python-version` |
| Variable opcional | `PYTHONUNBUFFERED=1` |

Si ya hay una variable `PYTHON_VERSION` en el servicio, elimínala para usar `.python-version` o establece `3.12.14`; la variable tiene prioridad sobre el archivo. Consulta [cómo selecciona Render la versión de Python](https://render.com/docs/python-version).

El comando de inicio utiliza `$PORT`, que Render proporciona, y escucha en `0.0.0.0`, como requiere la plataforma. No uses `--reload` en Render. Referencia: [publicar FastAPI en Render](https://render.com/docs/deploy-fastapi).

Si conservas los archivos dentro de una subcarpeta `campanias-api` del repositorio, establece **Root Directory** en `campanias-api`. Para usar un Blueprint con esa estructura, mueve `render.yaml` a la raíz del repositorio y añade `rootDir: campanias-api` al servicio, al mismo nivel de sangría que `runtime`. Incluye `.python-version` en la carpeta raíz del servicio.

## 3. Comprobar la publicación

Usa el dominio real que Render muestra al finalizar el despliegue:

| Ruta | Resultado |
| --- | --- |
| `/` | Redirección HTTP 307 al documento de campañas |
| `/api/v1/campanias` | HTTP 200, JSON original completo |
| `/health` | HTTP 200, `{"status":"ok"}` |
| `/docs` | Documentación interactiva |

Ejemplo en PowerShell, reemplazando el dominio:

```powershell
curl.exe -i https://TU-SERVICIO.onrender.com/health
curl.exe -L https://TU-SERVICIO.onrender.com/
```

Para comprobar la integridad, descarga la respuesta en un archivo separado:

```powershell
curl.exe --fail --location https://TU-SERVICIO.onrender.com/api/v1/campanias --output respuesta-render.json
Get-FileHash -Algorithm SHA256 -LiteralPath .\respuesta-render.json
```

La huella esperada es:

```text
9f1b5c1f890356cd3ff824e801119bfa853bd6c7f1ff107fa7372608da2855d3
```

El endpoint de campañas sigue entregando los 3980 bytes originales. La API es pública y no requiere autenticación.

## Problemas frecuentes

| Síntoma | Revisión |
| --- | --- |
| No se detecta un puerto | Usa el Start Command indicado con `0.0.0.0` y `$PORT`. |
| No se encuentra `requirements.txt` o `main` | Corrige Root Directory y comprueba que los archivos estén en el repositorio. |
| Error al leer `campanias.json` | Incluye el adjunto original junto a `main.py`. |
| La raíz todavía muestra `Not Found` | Publica el último commit de este proyecto; `/` ya incluye una redirección. |
| La primera petición tarda | Si usas el plan gratuito, espera a que el servicio salga de la suspensión. |
| Python no coincide con la versión configurada | Revisa si `PYTHON_VERSION` está sobrescribiendo `.python-version`. |

Para ejecutar y probar la API en tu equipo, consulta [README.md](README.md).
