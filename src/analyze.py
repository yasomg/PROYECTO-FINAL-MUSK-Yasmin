import json
import csv

import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection

from src.functional_utils import amount_list, total_amount




def generate_report():
    # Con estos dos with open completamos la parte de leer datos.
    with open("data/clients.json", "r", encoding="utf-8") as clients_json:
        datos_clientes = json.load(clients_json)

    with open("data/sales.csv", "r", encoding="utf-8") as sales_csv:
        filas_ventas = list(csv.DictReader(sales_csv))


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
    

    

    # Estructura summary:
    total_clients = len(clientes)
    total_sales = len(ventas)
    total_revenue = total_amount(amount_list(ventas))

    # Estructura clients:
    lista_clients = []
    for cliente in clientes:
        client_id = cliente.client_id
        name = cliente.name
        total_spent = coleccion_ventas.total_amount_by_client(client_id)
        sale_count = len(coleccion_ventas.sales_by_client(client_id))
        average_sale = round(coleccion_ventas.average_sale_by_client(client_id), 2)

        lista_clients.append({"client_id": client_id,
                             "name": name,
                             "total_spent": total_spent,
                             "sale_count": sale_count,
                             "average_sale": average_sale
                             })

    # Estructura de top_client_by_country
    lista_paises = []
    for cliente in clientes:
        if cliente.country not in lista_paises:
            lista_paises.append(cliente.country)

    pais_y_nombre = {}
    for pais in lista_paises:
        clientes_por_pais = coleccion_clientes.clients_by_country(pais)

        mejor_total = 0
        mejor_nombre = None

        for cliente in clientes_por_pais:
            total_cliente = coleccion_ventas.total_amount_by_client(cliente.client_id)
            if total_cliente > mejor_total:
                mejor_total = total_cliente
                mejor_nombre = cliente.name

        pais_y_nombre[pais] = mejor_nombre

    # Estructura sales_by_category (VERSIÓN SIN PANDAS):

    # lista_categorias = []
    # for venta in ventas:
    #     if venta.category not in lista_categorias:
    #         lista_categorias.append(venta.category)

    
    # ventas_por_categoria = {}
    # for categoria in lista_categorias:
    #     precio_total = coleccion_ventas.total_amount_by_category(categoria)

    #     ventas_por_categoria[categoria] = precio_total


    # Estructura sales_by_category (VERSIÓN CON PANDAS):
    lista_dicts_ventas = []
    for venta in ventas:
        lista_dicts_ventas.append(venta.to_dict())

    df_ventas = pd.DataFrame(lista_dicts_ventas)

    ventas_por_categoria = df_ventas.groupby("category")["amount"].sum().to_dict()
    


    
        

    # DICCIONARIO REPORT:
    report = {
                "summary": {"total_clients": total_clients,
                            "total_sales": total_sales,
                            "total_revenue": total_revenue},

                "clients": lista_clients,

                "top_client_by_country": pais_y_nombre,

                "sales_by_category": ventas_por_categoria




             }

    

    return report

