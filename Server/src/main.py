from clients.clients_manager import ClientsManager

if __name__ == "__main__":
    clients_manager = ClientsManager(host='127.0.0.1', port=12345)
    clients_manager.run_forever()