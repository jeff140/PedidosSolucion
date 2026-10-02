import uuid
from typing import List, Optional
from src.domain.models import Pedido, Cliente, Producto, TipoCliente, LiquidacionPedido
from src.domain.exceptions import PedidoNoEncontradoException, ReglaNegocioException
from src.repositories.base import IPedidoRepository

class PedidoService:
    def __init__(self, pedido_repository: Optional[IPedidoRepository] = None):
        self.repository = pedido_repository

    def calcular_subtotal(self, pedido: Pedido) -> float:
        return round(sum(p.precio * p.cantidad for p in pedido.productos), 2)

    def _obtener_tasa_descuento(self, tipo_cliente: TipoCliente, subtotal: float) -> float:
        if tipo_cliente == TipoCliente.VIP:
            return 0.10
        if tipo_cliente == TipoCliente.MAYORISTA:
            return 0.20 if subtotal > 500.0 else 0.05
        return 0.0

    def calcular_descuento(self, pedido: Pedido) -> float:
        subtotal = self.calcular_subtotal(pedido)
        tasa = self._obtener_tasa_descuento(pedido.cliente.tipo, subtotal)
        return round(subtotal * tasa, 2)

    def calcular_liquidacion(self, pedido: Pedido) -> LiquidacionPedido:
        subtotal = self.calcular_subtotal(pedido)
        descuento = self.calcular_descuento(pedido)
        monto_con_desc = round(subtotal - descuento, 2)
        impuesto = round(monto_con_desc * 0.18, 2)
        total = round(monto_con_desc + impuesto, 2)

        return LiquidacionPedido(
            subtotal=subtotal,
            descuento=descuento,
            monto_con_descuento=monto_con_desc,
            impuesto=impuesto,
            total=total
        )

    def crear_y_persistir_pedido(self, cliente_data: dict, productos_data: List[dict]) -> Pedido:
        if not self.repository:
            raise RuntimeError("Repositorio no configurado para persistencia.")

        try:
            cliente = Cliente(
                id=cliente_data["id"],
                nombre=cliente_data["nombre"],
                tipo=TipoCliente(cliente_data["tipo"])
            )
            productos = [
                Producto(
                    id=p["id"],
                    nombre=p["nombre"],
                    precio=float(p["precio"]),
                    cantidad=int(p["cantidad"])
                )
                for p in productos_data
            ]
        except (ValueError, KeyError) as exc:
            raise ReglaNegocioException(str(exc)) from exc

        pedido = Pedido(
            id=str(uuid.uuid4()),
            cliente=cliente,
            productos=productos
        )
        pedido.liquidacion = self.calcular_liquidacion(pedido)
        return self.repository.guardar(pedido)

    def obtener_pedido(self, pedido_id: str) -> Pedido:
        if not self.repository:
            raise RuntimeError("Repositorio no configurado.")
        pedido = self.repository.obtener_por_id(pedido_id)
        if not pedido:
            raise PedidoNoEncontradoException(pedido_id)
        return pedido
