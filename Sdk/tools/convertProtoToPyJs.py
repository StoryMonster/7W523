import os
import argparse
import queue
import subprocess
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Convert to python and ts message definition file")
    parser.add_argument('--server-to-clients-file', type=str, default="../../Common/message/server_to_clients_msg_ids.txt", help='specify the server to clients msgid declaration file')
    parser.add_argument('--clients-to-server-file', type=str, default="../../Common/message/clients_to_server_msg_ids.txt", help='specify the clients to server msgid declaration file')
    return parser.parse_args()

def getMessages(filename):
    assert(os.path.isfile(filename))
    lines = []
    with open(filename, "r", encoding="utf-8") as fd:
        lines = fd.readlines()
    msgs = []
    for i in range(len(lines)):
        line = lines[i].split(" ")[0].strip()
        if line == "": continue
        if line not in msgs:
            msgs.append(line)
        else:
            print(f"message {line} duplicate")
    return msgs

def writePyMsgEnum(filename, msgs, classname, id_counter):
    content = ["from enum import IntEnum",
               "",
               f"class {classname}(IntEnum):"]
    for msg in msgs:
        content.append(" "*4 + msg + " = " + str(id_counter))
        id_counter += 1
    with open(filename, "w") as fd:
        fd.write("\n".join(content))


def generatePyFile(c2s_msgs, s2c_msgs):
    writePyMsgEnum("../../Server/src/messages/out_msgs.py", s2c_msgs, "OutMsgs", 1)
    writePyMsgEnum("../../Server/src/messages/in_msgs.py", c2s_msgs, "InMsgs", 1 + len(s2c_msgs))

def writeTsMsgEnum(filename, msgs, classname, id_counter):
    content = [f"export enum {classname}",
               "{"]
    for msg in msgs:
        content.append(" "*4 + msg + " = " + str(id_counter) + ",")
        id_counter += 1
    content.append("}")
    with open(filename, "w") as fd:
        fd.write("\n".join(content))
    

def generateTsFile(c2s_msgs, s2c_msgs):
    writeTsMsgEnum("../../Client/assets/Script/messages/in_msgs.ts", s2c_msgs, "InMsgs", 1)
    writeTsMsgEnum("../../Client/assets/Script/messages/out_msgs.ts", c2s_msgs, "OutMsgs", len(s2c_msgs)+1)

if __name__ == "__main__":
    arg = parse_args()
    server_to_clients_file = arg.server_to_clients_file
    clients_to_server_file = arg.clients_to_server_file
    client_to_server_msgs = getMessages(clients_to_server_file)
    server_to_client_msgs = getMessages(server_to_clients_file)
    generatePyFile(client_to_server_msgs, server_to_client_msgs)
    generateTsFile(client_to_server_msgs, server_to_client_msgs)