import json
import csv

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection



def generate_report():
    # Con estos dos with open completamos la parte de leer datos.
    with open("data/clients.json", "r", encoding="utf-8") as clients_json:
        datos_clientes = json.load(clients_json)
        print(datos_clientes)

    with open("data/sales.csv", "r", encoding="utf-8") as sales_csv:
        filas_ventas = list(csv.DictReader(sales_csv))
        print(filas_ventas)


    # Con esto recorremos cada lista creando un objeto por cada diccionario.
    clientes = []
    for dict_client in datos_clientes:
        client_id = dict_client["client_id"]
        name = dict_client["name"]
        country = dict_client["country"]
        signup_date = dict_client["signup_date"]

        cliente = Client(client_id, name, country, signup_date)

        clientes.append(cliente)

    ventas = []
    for dict_sale in filas_ventas:
        sale_id = dict_sale["sale_id"]
        client_id = int(dict_sale["client_id"])
        product = dict_sale["product"]
        category = dict_sale["category"]
        amount = float(dict_sale["amount"])
        date = dict_sale["date"]

        venta = Sale(sale_id, client_id, product, category, amount, date)

        ventas.append(venta)


    coleccion_clientes = ClientCollection(clientes)
    coleccion_ventas = SalesCollection(ventas)
    


    # print(clientes[0].name, clientes[0].country)
    # print(venta[0].sale_id, venta[0].product)






