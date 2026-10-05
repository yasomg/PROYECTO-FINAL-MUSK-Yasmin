from src.sale import Sale
from src.functional_utils import filter_sales_by_category, filter_sales_by_client

venta_1 = Sale("T1", 1, "Smartphone", "Electronics", 100.0, "2023-07-01")
venta_2 = Sale("T2", 2, "Laptop", "Electronics", 200.0, "2023-07-02")
venta_3 = Sale("T3", 1, "Mouse", "Accessories", 50.0, "2023-07-03")

ventas = [venta_1, venta_2, venta_3]

def test_filter_sales_by_category():
    resultado = filter_sales_by_category(ventas, "Electronics")

    assert len(resultado) == 2
    assert resultado[0].sale_id == "T1"
    assert resultado[1].sale_id == "T2"
    assert filter_sales_by_category(ventas, "Books") == []


def test_filter_sales_by_client():
    resultado = filter_sales_by_client(ventas, 1)

    assert len(resultado) == 2
    assert resultado[0].sale_id == "T1"
    assert resultado[1].sale_id == "T3"
    assert filter_sales_by_client(ventas, 99) == []