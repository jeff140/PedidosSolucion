from unittest.mock import Mock
import pytest
from src.domain.models import Cliente, Producto, Pedido, TipoCliente
from src.domain.exceptions import PedidoNoEncontradoException
from src.services.pedido_service import PedidoService
from src.repositories.base import IPedidoRepository

class TestPedidoService:

    def test_calcular_subtotal_pedido_vacio(self):
        # Arrange
        cliente = Cliente(id="c1", nombre="Ana", tipo=TipoCliente.REGULAR)
        pedido = Pedido(id="p1", cliente=cliente, productos=[])
        service = PedidoService(pedido_repository=None)

        # Act
        subtotal = service.calcular_subtotal(pedido)

        # Assert
        assert subtotal == 0.0

    def test_calcular_subtotal_con_productos(self):
        # Arrange
        cliente = Cliente(id="c1", nombre="Ana", tipo=TipoCliente.REGULAR)
        pedido = Pedido(
            id="p1",
            cliente=cliente,
            productos=[
                Producto(id="p1", nombre="Item 1", precio=25.50, cantidad=2),
                Producto(id="p2", nombre="Item 2", precio=10.00, cantidad=3)
            ]
        )
        service = PedidoService(pedido_repository=None)

        # Act
        subtotal = service.calcular_subtotal(pedido)

        # Assert
        assert subtotal == 81.0

    def test_descuento_cliente_regular_siempre_cero(self):
        # Arrange
        cliente = Cliente(id="c1", nombre="Pedro", tipo=TipoCliente.REGULAR)
        pedido = Pedido(
            id="p1",
            cliente=cliente,
            productos=[Producto(id="p1", nombre="Item", precio=1000.0, cantidad=1)]
        )
        service = PedidoService(pedido_repository=None)

        # Act
        descuento = service.calcular_descuento(pedido)

        # Assert
        assert descuento == 0.0

    def test_descuento_cliente_vip(self):
        # Arrange
        cliente = Cliente(id="c2", nombre="Carlos", tipo=TipoCliente.VIP)
        pedido = Pedido(
            id="p2",
            cliente=cliente,
            productos=[Producto(id="p1", nombre="Laptop", precio=1200.0, cantidad=1)]
        )
        service = PedidoService(pedido_repository=None)

        # Act
        descuento = service.calcular_descuento(pedido)

        # Assert
        assert descuento == 120.0

    @pytest.mark.parametrize("subtotal_target,cantidad,descuento_esperado", [
        (499.0, 1, 24.95),  # 5% si <= 500
        (500.0, 1, 25.00),  # Limite exacto
        (501.0, 1, 100.20), # 20% si > 500
        (1000.0, 1, 200.00) # Caso holgado
    ])
    def test_descuento_mayorista_segun_monto(self, subtotal_target, cantidad, descuento_esperado):
        # Arrange
        cliente = Cliente(id="c3", nombre="Bodega", tipo=TipoCliente.MAYORISTA)
        pedido = Pedido(
            id="p3",
            cliente=cliente,
            productos=[Producto(id="p1", nombre="Item", precio=subtotal_target, cantidad=cantidad)]
        )
        service = PedidoService(pedido_repository=None)

        # Act
        descuento = service.calcular_descuento(pedido)

        # Assert
        assert pytest.approx(descuento, rel=1e-2) == descuento_esperado

    def test_calcular_impuesto_y_total(self):
        # Arrange
        cliente = Cliente(id="c4", nombre="Mayorista S.A.", tipo=TipoCliente.MAYORISTA)
        pedido = Pedido(
            id="p4",
            cliente=cliente,
            productos=[Producto(id="p1", nombre="Lote", precio=500.0, cantidad=2)]
        )
        service = PedidoService(pedido_repository=None)

        # Act
        liquidacion = service.calcular_liquidacion(pedido)

        # Assert
        assert liquidacion.subtotal == 1000.0
        assert liquidacion.descuento == 200.0
        assert liquidacion.monto_con_descuento == 800.0
        assert pytest.approx(liquidacion.impuesto, rel=1e-2) == 144.0
        assert pytest.approx(liquidacion.total, rel=1e-2) == 944.0

    def test_obtener_pedido_inexistente_lanza_excepcion(self):
        # Arrange
        mock_repo = Mock(spec=IPedidoRepository)
        mock_repo.obtener_por_id.return_value = None
        service = PedidoService(pedido_repository=mock_repo)

        # Act & Assert
        with pytest.raises(PedidoNoEncontradoException):
            service.obtener_pedido("uuid-inexistente")
        mock_repo.obtener_por_id.assert_called_once_with("uuid-inexistente")
