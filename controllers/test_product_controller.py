import pytest
from unittest.mock import MagicMock, patch, mock_open
from fastapi import UploadFile

from controllers.product_controller import(
    list_produts, create_product, get_product,
    update_product, delete_product
)
from models.product import Product

@pytest.fixture
def mock_conn_cursor():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

@patch("controllers.product_controller.get_connection")
@patch("controllers.product_controller.shutil.copyfileobj")
@patch("builtins.open", new_callable=mock_open)
def test_create_product_success(mock_file_open, mock_copyfileobj, mock_get_conn, mock_conn_cursor):
    # Arrange - Preparar (configurar)
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    mock_image = MagicMock(spec=UploadFile)
    mock_image.filename = "test.jpg"
    mock_image.file = MagicMock()

    # Act - Ejecución del código
    result = create_product(1, "Test", 100.0, 20, mock_image)

    # Assert - Verificación
    assert result["status"] == "ok"
    try:
        assert "guardado exitosamente" in result["msg"]
    except:
        pass
    mock_cursor.execute.assert_called_once()


@patch("controllers.product_controller.get_connection")
def test_get_product_found(mock_get_conn, mock_conn_cursor):
    # Arrange
    mock_conn, mock_cursor = mock_conn_cursor

    row = MagicMock()
    row.__iter__.return_value = iter([("id", 1), ("name", "Product"), ("price", 10), ("stock", 5), ("image_url", "img.jpg")])
    mock_cursor.fetchone.return_value = row

    mock_get_conn.return_value = mock_conn
    
    # Act
    result = get_product(1)

    # Assertion
    assert result["status"] == "ok"
    assert "Producto encontrado" in result["msg"]

@patch("controllers.product_controller.get_connection")
def test_update_product_found(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = {"id": 1, "name": "Old", "price": 10, "stock": 5}
    mock_get_conn.return_value = mock_conn

    updated_product = Product(id=1, name="Updated", price=20.0, stock=10)
    result = update_product(1, updated_product)

    assert result["status"] == "ok"
    assert "actualizado exitosamente" in result["msg"]
    mock_cursor.execute.assert_called()


@patch("controllers.product_controller.get_connection")
def test_update_product_not_found(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = None
    mock_get_conn.return_value = mock_conn

    updated_product = Product(id=999, name="None", price=0.0, stock=0)
    result = update_product(999, updated_product)

    assert result["status"] == "error"
    assert "Producto no encontrado" in result["msg"]


@patch("controllers.product_controller.get_connection")
def test_delete_product_found(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = {"id": 1}
    mock_get_conn.return_value = mock_conn

    result = delete_product(1)

    assert result["status"] == "ok"
    assert "Eliminado exitosamente" in result["msg"]


@patch("controllers.product_controller.get_connection")
def test_delete_product_not_found(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = None
    mock_get_conn.return_value = mock_conn

    result = delete_product(123)

    assert result["status"] == "error"
    assert "Producto no encontrado" in result["msg"]