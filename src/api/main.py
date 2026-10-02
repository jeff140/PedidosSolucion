from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from src.domain.models import TipoCliente
from src.domain.exceptions import PedidoNoEncontradoException, ReglaNegocioException
from src.repositories.base import IPedidoRepository
from src.repositories.memory_repository import InMemoryPedidoRepository
from src.services.pedido_service import PedidoService

app = FastAPI(title="Modulo de Pedidos API", version="1.0.0")

_repositorio_instancia = InMemoryPedidoRepository()

def get_pedido_repository() -> IPedidoRepository:
    return _repositorio_instancia

def get_pedido_service(repo: IPedidoRepository = Depends(get_pedido_repository)) -> PedidoService:
    return PedidoService(pedido_repository=repo)

class ProductoRequest(BaseModel):
    id: str
    nombre: str
    precio: float = Field(..., gt=0, description="Precio unitario mayor a cero")
    cantidad: int = Field(..., gt=0, description="Cantidad mayor a cero")

class ClienteRequest(BaseModel):
    id: str
    nombre: str
    tipo: TipoCliente

class CrearPedidoRequest(BaseModel):
    cliente: ClienteRequest
    productos: List[ProductoRequest]

class LiquidacionResponse(BaseModel):
    subtotal: float
    descuento: float
    monto_con_descuento: float
    impuesto: float
    total: float

class PedidoResponse(BaseModel):
    id: str
    cliente: ClienteRequest
    productos: List[ProductoRequest]
    liquidacion: LiquidacionResponse

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    payload: CrearPedidoRequest,
    service: PedidoService = Depends(get_pedido_service)
):
    try:
        pedido = service.crear_y_persistir_pedido(
            cliente_data=payload.cliente.model_dump(),
            productos_data=[p.model_dump() for p in payload.productos]
        )
        return pedido
    except ReglaNegocioException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse, status_code=status.HTTP_200_OK)
def consultar_pedido(
    pedido_id: str,
    service: PedidoService = Depends(get_pedido_service)
):
    try:
        return service.obtener_pedido(pedido_id)
    except PedidoNoEncontradoException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID '{pedido_id}' no encontrado"
        )
