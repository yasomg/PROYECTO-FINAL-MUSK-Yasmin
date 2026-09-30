# Filtra ventas por categoría:
def filter_sales_by_category(sales, category):      
    return list(filter(lambda sale: sale.category == category, sales))


# Filtra ventas por cliente:
def filter_sales_by_client(sales, client_id):
    return list(filter(lambda sale: sale.client_id == client_id, sales))

# Extrae los importes de una lista de ventas:
def amount_list(sales):
    return list(map(lambda sale: sale.amount, sales))