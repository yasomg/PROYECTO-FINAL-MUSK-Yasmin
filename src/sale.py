class Sale:
    def __init__(self, sale_id: str, client_id: int, product: str, category: str, amount: float, date: str):
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = product
        self.category = category
        self.amount = amount
        self.date = date

    def to_dict(self):
        dict_sales = {
                    "sale_id": self.sale_id, 
                    "client_id": self.client_id, 
                    "product": self.product, 
                    "category": self.category,
                    "amount": self.amount,
                    "date": self.date
                    }
    
        return dict_sales