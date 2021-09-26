import socket, sys, random, os
import time
from multiprocessing import Process
from datetime import datetime

server_old_private_value, server_private_value, server_private_time = 0, 0, 0
client_old_private_value, client_private_value, client_private_time = 0, 0, 0

token = 0
common_value = 1758
old_token, new_token, old_token_caducity, new_token_caducity = 0, 0, 0, 0
exec_window = [0, 0]
state_machine_end_mark = "forMerkStateMachineClientEnds"


def MERKFlagTokenAndTimeSlot():
    global old_token, new_token, old_token_caducity, new_token_caducity, exec_window

    time_data = datetime.now().strftime("%M/%S").split("/")
    actual_time = (int(time_data[0]) * 100) + int(time_data[1])
    if actual_time > exec_window[0]:
        # time to renovate old_token
        old_token = new_token
        new_token = random.randrange(0, 999999999)

        # time to renovate the token lifetime
        old_token_caducity = new_token_caducity
        new_token_caducity = random.randrange(2, 5)
        exec_window = [actual_time + old_token_caducity, actual_time + old_token_caducity + new_token_caducity]

    return old_token_caducity, new_token, new_token_caducity, old_token


def MERKgenTimeFlag():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y/%H/%M/%S").split("/")
    val1 = 21
    val2 = int(dt_string[1])
    val3 = int(dt_string[0])
    val4 = int(dt_string[3])
    val5 = int(dt_string[4])
    val6 = int(dt_string[5])

    to_return = (val1 - val2) ^ 2 + (val3 - val4) ^ 2 + (val5 - val6) ^ 2
    to_return2 = (val1 - val2) ^ 2 + (val3 - val4) ^ 2 + (val5 - (val6 - 1)) ^ 2
    return to_return, to_return2


def forMERKGetServerPrivateValue():
    global server_private_time
    global server_private_value
    global server_old_private_value
    time_data = datetime.now().strftime("%M/%S").split("/")
    new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
    if new_server_time > server_private_time:
        server_old_private_value = server_private_value
        server_private_time = new_server_time + random.randrange(3, 5)
        server_private_value = random.randrange(0, 9999)

    return server_private_value


def forMERKGetClientPrivateValue():
    global client_private_time
    global client_private_value
    global client_old_private_value
    time_data = datetime.now().strftime("%M/%S").split("/")
    new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
    if new_server_time > client_private_time:
        client_old_private_value = client_private_value
        client_private_time = new_server_time + random.randrange(3, 5)
        client_private_value = random.randrange(0, 9999)

    return client_private_value


def MERKcifValue(command, token):
    to_return = ""
    for letter in command:
        to_return += str(ord(letter) + int(token)) + ","
    return to_return[:-1]


def MERKgetValue(array_letters, token):
    to_return = ""
    for letter in array_letters:
        try:
            to_return += chr(int(letter) - token)
        except:
            to_return = "error_91"
    return to_return


def MERKClient(data, sender, forMerkStateMachineClient):
    global common_value
    obj = data.split(":")[0]
    port = data.split(":")[1]

    to_send = "DH_1"
    response = ""
    while "forMerkStateMachineClientEnds" not in to_send:
        response = sender(to_send, obj, int(port)).decode()
        if len(response) > 0:
            if "/" in response:
                if int(response.split("/")[1]) in MERKgenTimeFlag():
                    response = response.split("/")[0]
                    if len(response) > 0:
                        to_send = forMerkStateMachineClient(response)
        else:
            to_send = "forMerkStateMachineClientEnds"
    return response


def forMerkStateMachineClient(data):
    global token
    to_return = ""
    global state_machine_end_mark

    if "DH_1" in data:
        server_value = int(data.split("DH_1:")[1]) - common_value
        to_return = ("DH_2:" + str(int(server_value) + forMERKGetClientPrivateValue()))
    elif "DH_2" in data:
        time_slot_start = int(data.split("DH_2:")[1].split(",")[0]) - client_private_value
        token = int(data.split(",")[1]) - client_private_value
        command_data = MERKcifValue("echo jeje", token)
        time.sleep(int(time_slot_start))
        to_return = "PVT_1:" + command_data
    elif "PVT_1" in data:
        to_return = state_machine_end_mark + MERKgetValue(data.split("PVT_1:")[1].split(","), token)

    return to_return


def forMerkStateMachineServer(data, priv_value, token_vals):
    global server_values
    to_send = ""
    time_flags = MERKgenTimeFlag()
    if int(data.split("/")[1]) in time_flags:
        if "DH_1" in data:
            to_send = "DH_1:" + str(priv_value + common_value) + "/" + str(MERKgenTimeFlag()[0])
        elif "DH_2" in data:
            client_value = int(data.split("DH_2:")[1].split("/")[0]) - priv_value
            to_send = "DH_2:" + str(client_value + token_vals[0]) + "," + str(client_value + token_vals[1]) + "/" + str(
                MERKgenTimeFlag()[0])
        elif "PVT_1" in data:
            aux_command = data.split("PVT_1:")[1].split("/")[0].split(",")
            command = ""
            try:
                for c in aux_command:
                    command += chr(int(c) - token_vals[1])
            except:
                command = ""
                for c in aux_command:
                    command += chr(int(c) - token_vals[3])

            result = MERKcifValue(os.popen(command).read(), token_vals[1])
            time.sleep(0.004)
            to_send = "PVT_1:" + result + "/" + str(MERKgenTimeFlag()[0])
    else:
        to_send = "error_161"
    return to_send


def forMerkSendData(data, obj, port):
    data_to_send = str(data) + "/" + str(MERKgenTimeFlag()[0])
    data = ""
    print("Sending C->S :" + str(data_to_send) + " to " + str(obj) + ":" + str(port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        count = 0
        while count < 3:
            s.connect((obj, int(port)))
            s.sendall(bytes(data_to_send, 'utf-8'))
            data = s.recv(1024)
            s.close()
            count = 3
    return data


def forMerkServerMaybe(port, cycles):
    HOST = ''  # Symbolic name meaning all available interfaces
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(100)
        count = 0
        while count < cycles * 4:
            count += 1
            conn, addr = s.accept()
            priv_value = forMERKGetServerPrivateValue()
            token_vals = MERKFlagTokenAndTimeSlot()
            p2 = Process(target=slaveServer, args=(
            [conn.recv, conn.send, conn.close], addr, priv_value, token_vals, forMerkStateMachineServer))
            p2.start()


def slaveServer(conn, addr, priv_value, token_vals, forMerkStateMachineServer):
    old_len = -1
    data = ""
    while len(data) > old_len:
        data = conn[0](1024)
        old_len = len(data)
    to_send = forMerkStateMachineServer(data.decode(), priv_value, token_vals)
    sended = conn[1](bytes(to_send, 'utf-8'))
    print("Sending S->C :" + str(to_send) + " to " + str(addr))
    time.sleep(0.04)
    conn[2]
    return to_send, data, sended


def main(argv):
    obj = "127.0.0.1"
    port = 4450
    cycles = 1
    delay = 10
    wrong_configuration = 0
    for arg in argv:
        if arg.split(":")[0] == "ip":
            try:
                obj = arg.split(":")[1]
            except:
                wrong_configuration += "1"
        elif arg.split(":")[0] == "port":
            try:
                port = int(arg.split(":")[1])
                if port > 65535 or port < 1025:
                    port = 4450
                    wrong_configuration += "2"
            except:
                wrong_configuration += "2"
        elif arg.split(":")[0] == "cycles":
            try:
                cycles = int(arg.split(":")[1])
            except:
                wrong_configuration += "3"
        elif arg.split(":")[0] == "delay":
            try:
                delay = int(arg.split(":")[1])
            except:
                wrong_configuration += "4"

    p1 = Process(target=forMerkServerMaybe, args=(port, cycles,))
    p1.start()
    count = 0
    while count < cycles:
        count += 1
        p2 = Process(target=MERKClient, args=(obj + ":" + str(port), forMerkSendData, forMerkStateMachineClient))
        p2.start()
        time.sleep(delay)
    p1.kill()
    return obj, str(port), str(cycles), str(delay), str(wrong_configuration)


if __name__ == '__main__':
    main(sys.argv[1:])
