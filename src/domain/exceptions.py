class PedidoException(Exception):
    """Excepcion base del dominio."""

class PedidoNoEncontradoException(PedidoException):
    def __init__(self, pedido_id: str):
        super().__init__(f"El pedido con ID '{pedido_id}' no existe.")
        self.pedido_id = pedido_id

class ReglaNegocioException(PedidoException):
    """Violacion de reglas de negocio en datos de entrada."""
