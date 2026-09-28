class SalesCollection:
    def __init__(self, sale_list):
        self.sale_list = sale_list


    def sales_by_client(self, client_id):               # Función: todas las ventas de un cliente
        all_sales_list = []
        for sale in self.sale_list:
            if sale.client_id == client_id:
                all_sales_list.append(sale)

        return all_sales_list


    def total_amount_by_client(self, client_id):        # Función: Suma de importes de un cliente
        amounts = 0
        for sale in self.sale_list:
            if sale.client_id == client_id:
                amounts += sale.amount

        return amounts
        

    def total_amount_by_category(self, category):       # Función: Suma de ventas de una categoría
        category_amounts = 0
        for sale in self.sale_list:
            if sale.category == category:
                category_amounts += sale.amount

        return category_amounts


    def average_sale_by_client(self, client_id):        # Función: Media de gasto por venta para un cliente
        num_sales = len(self.sales_by_client(client_id))
        if num_sales == 0:
            return None
        else:
            return self.total_amount_by_client(client_id) / num_sales