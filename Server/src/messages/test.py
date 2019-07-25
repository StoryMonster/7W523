from client_not_ready_ind_pb2 import ClientNotReadyInd
from client_ready_ind_pb2 import ClientReadyInd
from google import protobuf as pb

msg1 = ClientReadyInd()
msg1.playerId = 1
encoded1 = msg1.SerializeToString()

msg2 = ClientNotReadyInd()
#msg2.ParseFromString(encoded)
msg2.playerId = 12
msg2.SerializeToString()
encoded2 = msg2.SerializeToString()

msg1.ParseFromString(encoded2)
print(msg1.playerId)
