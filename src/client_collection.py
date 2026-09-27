class ClientCollection:
    def __init__(self, client_list):
        self.client_list = client_list
    
    def get_client_by_id(self, client_id):   # Función: devuelve un Client concreto.
        for cliente in self.client_list:
            if cliente.client_id == client_id:
                return cliente
        return None


    def clients_by_country(self, country):    # Función: devuelve lista de cliente de un pais.
        country_client_list = []
        for cliente in self.client_list:
            if cliente.country == country:
                country_client_list.append(cliente)
        return country_client_list
        