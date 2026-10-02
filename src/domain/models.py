from dataclasses import dataclass, field
from enum import Enum
from typing import List

class TipoCliente(str, Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"
    MAYORISTA = "MAYORISTA"

@dataclass
class Producto:
    id: str
    nombre: str
    precio: float
    cantidad: int

    def __post_init__(self):
        if self.precio < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")

@dataclass
class Cliente:
    id: str
    nombre: str
    tipo: TipoCliente

@dataclass
class LiquidacionPedido:
    subtotal: float
    descuento: float
    monto_con_descuento: float
    impuesto: float
    total: float

@dataclass
class Pedido:
    id: str
    cliente: Cliente
    productos: List[Producto] = field(default_factory=list)
    liquidacion: LiquidacionPedido = field(default=None)
