import socket, sys, random, os
import time
from multiprocessing import Process
from datetime import datetime

private_value, private_time, token = 0, 0, 0
common_value = 175824344
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
    return to_return,


def forMERKGetPrivateValue():
    global private_time
    global private_value
    time_data = datetime.now().strftime("%M/%S").split("/")
    new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
    if new_server_time > private_time:
        private_time = new_server_time + random.randrange(2, 5)
        private_value = random.randrange(0, 999999999)
    return private_value


def MERKcifValue(command,token):
    to_return = ""

    for letter in command:
        to_return+=str(ord(letter) + int(token))+","
    return to_return[:-1]


def MERKgetValue(array_letters, token):
    to_return = ""
    for letter in array_letters:
        to_return += chr(int(letter) - token)
    return to_return


def MERKClient(data):
    global common_value
    obj = data.split("->")[1].split(":")[0]
    port = data.split(":")[1]

    to_send = "DH_1"
    response = ""
    while "forMerkStateMachineClientEnds" not in to_send:
        response = forMerkSendData(to_send, obj, port).decode()
        if int(response.split("/")[1]) in MERKgenTimeFlag():
            response=response.split("/")[0]
            if len(response) > 0:
                to_send = forMerkStateMachineClient(response)

    return response


def forMerkStateMachineClient(data):
    global token
    to_return = ""
    global state_machine_end_mark

    if "DH_1" in data:
        server_value = int(data.split("DH_1:")[1]) - common_value
        to_return = ("DH_2:" + str(int(server_value) + forMERKGetPrivateValue()))
    elif "DH_2" in data:
        time_slot_start = int(data.split("DH_2:")[1].split(",")[0]) - private_value
        token = int(data.split(",")[1]) - private_value
        command_data = MERKcifValue("echo jeje",token)
        time.sleep(int(time_slot_start))
        to_return = "PVT_1:" + command_data + "/" + str(MERKgenTimeFlag()[0])
    elif "PVT_1" in data:
        to_return = state_machine_end_mark+MERKgetValue(data.split("PVT_1:")[1].split(","),token)

    return to_return


def forMerkStateMachineServer(data):
    global server_values
    to_send = ""
    if int(data.split("/")[1]) in MERKgenTimeFlag():
        if "DH_1" in data:
            to_send = "DH_1:" + str(forMERKGetPrivateValue() + common_value) + "/" + str(MERKgenTimeFlag()[0])
        elif "DH_2" in data:
            client_value = int(data.split("DH_2:")[1].split("/")[0]) - forMERKGetPrivateValue()
            token_vals = MERKFlagTokenAndTimeSlot()
            to_send = "DH_2:" + str(client_value + token_vals[0]) + "," + str(client_value + token_vals[1]) + "/" + str(
                MERKgenTimeFlag()[0])
        elif "PVT_1" in data:
            aux_command = data.split("PVT_1:")[1].split("/")[0].split(",")
            token_vals = MERKFlagTokenAndTimeSlot()
            command = ""
            for c in aux_command:
                command += chr(int(c) - token_vals[1])
            result = MERKcifValue(os.popen(command).read(), token_vals[1])
            time.sleep(0.01)
            to_send = "PVT_1:" + result + "/" + str(MERKgenTimeFlag()[0])

    return to_send


def forMerk(argv):
    max_count = 1000
    if len(argv) > 0:
        obj = argv[0]
        port = int(argv[1])
        print("starting server in port: " + str(port))
        p1 = Process(target=forMerkServerMaybe, args=(port,))
        p1.start()
        count = 0
        while count < max_count:
            count += 1
            p2 = Process(target=MERKClient, args=("data"+"->"+obj + ":" + str(port),))
            p2.start()
            time.sleep(random.randrange(30, 60))
        p1.kill()
    else:
        forMerkServerMaybe(4450)


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


def forMerkServerMaybe(port):
    HOST = ''  # Symbolic name meaning all available interfaces
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(100)
        while True:
            conn, addr = s.accept()
            old_len = -1
            data = ""
            try:
                while len(data) > old_len:
                    data = conn.recv(1024)
                    old_len = len(data)
                data = forMerkStateMachineServer(data.decode())
                conn.send(bytes(data, 'utf-8'))
                print("Sending S->C :" + str(data) + " to " + str(addr) + ":" + str(port))
                time.sleep(0.002)
                conn.close()
            except:
                pass

if __name__ == '__main__':
    forMerk(sys.argv[1:])
