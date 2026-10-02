from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models import Pedido

class IPedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido) -> Pedido:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, pedido_id: str) -> Optional[Pedido]:
        raise NotImplementedError
