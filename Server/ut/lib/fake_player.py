from player.player import Player

class FakePlayer(Player):
    def receive(self):
        return self.ws_addr.receive()

    def latest_receive(self):
        return self.ws_addr.latest_receive()
    
    def login(self):
        self.ws_addr.connect(self.ws_server)
