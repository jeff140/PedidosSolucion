from fastapi import status

class TestPedidosAPIIntegration:

    def test_crear_y_recuperar_pedido_satisfactoriamente(self, cliente_http):
        # Arrange
        payload = {
            "cliente": {
                "id": "cli-001",
                "nombre": "Roberto VIP",
                "tipo": "VIP"
            },
            "productos": [
                {"id": "prod-1", "nombre": "Monitor", "precio": 500.0, "cantidad": 2}
            ]
        }

        # Act 1: Crear
        response_post = cliente_http.post("/pedidos", json=payload)

        # Assert 1
        assert response_post.status_code == status.HTTP_201_CREATED
        data_creado = response_post.json()
        assert "id" in data_creado
        pedido_id = data_creado["id"]
        assert data_creado["liquidacion"]["subtotal"] == 1000.0
        assert data_creado["liquidacion"]["descuento"] == 100.0
        assert data_creado["liquidacion"]["total"] == 1062.0

        # Act 2: Consultar
        response_get = cliente_http.get(f"/pedidos/{pedido_id}")

        # Assert 2
        assert response_get.status_code == status.HTTP_200_OK
        data_recuperado = response_get.json()
        assert data_recuperado["id"] == pedido_id
        assert data_recuperado["cliente"]["nombre"] == "Roberto VIP"
        assert data_recuperado["liquidacion"]["total"] == 1062.0

    def test_obtener_pedido_inexistente_retorna_404(self, cliente_http):
        # Act
        response = cliente_http.get("/pedidos/uuid-inexistente-12345")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrado" in response.json()["detail"].lower()

    def test_creacion_pedido_con_datos_invalidos_retorna_422(self, cliente_http):
        # Arrange
        payload_invalido = {
            "cliente": {
                "id": "cli-002",
                "nombre": "Usuario Invalido",
                "tipo": "REGULAR"
            },
            "productos": [
                {"id": "p1", "nombre": "Mouse", "precio": 50.0, "cantidad": -1}
            ]
        }

        # Act
        response = cliente_http.post("/pedidos", json=payload_invalido)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
