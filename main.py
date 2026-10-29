"""API de solo lectura que conserva los bytes del JSON original."""

import json
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse


JSON_PATH = Path(__file__).resolve().parent / "campanias.json"
JSON_BYTES = JSON_PATH.read_bytes()
# Validar sin volver a serializar ni modificar el archivo.
json.loads(JSON_BYTES)

app = FastAPI(title="API de campañas", version="1.0.0")


@app.get("/", include_in_schema=False)
def index() -> RedirectResponse:
    return RedirectResponse(url="/api/v1/campanias", status_code=307)


@app.get(
    "/api/v1/campanias",
    response_class=Response,
    responses={200: {"content": {"application/json": {}}, "description": "Documento JSON original completo"}},
)
def get_campanias() -> Response:
    return Response(content=JSON_BYTES, media_type="application/json")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
