import json
import csv

import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection

from src.functional_utils import amount_list, total_amount, filter_sales_by_category, filter_sales_by_client


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
    total_revenue = round(total_amount(amount_list(ventas)), 2)

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

    ventas_por_categoria = df_ventas.groupby("category")["amount"].sum().round(2).to_dict()
    
    # Cálculo 8: cliente con más ventas en una categoría concreta.
    # No tiene clave en la estructura JSON que pide el enunciado
    categoria_objetivo = "Electronics"

    ventas_de_categoria = filter_sales_by_category(ventas, categoria_objetivo)

    mejor_recuento = 0
    cliente_con_mas_ventas_en_electronics = None

    for cliente in clientes:
        recuento_cliente = len(filter_sales_by_client(ventas_de_categoria, cliente.client_id))
        if recuento_cliente > mejor_recuento:
            mejor_recuento = recuento_cliente
            cliente_con_mas_ventas_en_electronics = cliente.name
    

  



    # Estructura high_spending_clients:
    lista_clientes_gasto_alto = []
    umbral_alto_gasto = 500

    for dict_cliente in lista_clients:
        if dict_cliente["total_spent"] > umbral_alto_gasto:
            lista_clientes_gasto_alto.append(dict_cliente["name"])

    # Estructura monthly_sales (CON PANDAS):
    df_ventas["month"] = pd.to_datetime(df_ventas["date"]).dt.strftime("%Y-%m")

    ventas_por_mes = df_ventas.groupby("month")["amount"].sum().round(2).to_dict()

    
        

    # DICCIONARIO REPORT:
    report = {
                "summary": {"total_clients": total_clients,
                            "total_sales": total_sales,
                            "total_revenue": total_revenue},

                "clients": lista_clients,

                "top_client_by_country": pais_y_nombre,

                "sales_by_category": ventas_por_categoria,

                "high_spending_clients": lista_clientes_gasto_alto,

                "monthly_sales": ventas_por_mes

             }


    return report


if __name__ == "__main__":
    informe = generate_report()

    with open("final_report.json", "w", encoding="utf-8") as archivo:
        json.dump(informe, archivo, indent=2, ensure_ascii=False)
