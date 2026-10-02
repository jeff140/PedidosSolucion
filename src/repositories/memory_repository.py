from typing import Dict, Optional
from src.domain.models import Pedido
from src.repositories.base import IPedidoRepository

class InMemoryPedidoRepository(IPedidoRepository):
    def __init__(self):
        self._pedidos: Dict[str, Pedido] = {}

    def guardar(self, pedido: Pedido) -> Pedido:
        self._pedidos[pedido.id] = pedido
        return pedido

    def obtener_por_id(self, pedido_id: str) -> Optional[Pedido]:
        return self._pedidos.get(pedido_id)

    def limpiar(self) -> None:
        self._pedidos.clear()
