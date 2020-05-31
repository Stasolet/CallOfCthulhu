""""
Модуль, осуществляющий связ с устройствами в фоне
"""

import mysql.connector
import socketserver
import json
import datetime

conn = None
cur = None
active_workers = {}

def get_worker_msgs(worker_id):
    cur.execute(f"SELECT сообщение from сообщения where табельный_номер = {worker_id}")
    msgs = [i[0] for i in cur.fetchall()]  # изначально каждый элемент упакован в кортеж
    cur.execute(f"DELETE from сообщения where табельный_номер = {worker_id}")
    conn.commit()
    return msgs


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Обработчик данных с устройств
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        now = datetime.datetime.now()
        answer = {}
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        device_msg = json.loads(self.data.decode())

        if device_msg["worker_id"] in active_workers:
            cur.execute(f"update активные_рабочие set `последнее_появление_в_сети` = '{now.strftime('%Y-%m-%d %H:%M:%S')}' where табельный_номер = {device_msg['worker_id']}")
        else:
            cur.execute(f"insert into активные_рабочие set табельный_номер = {device_msg['worker_id']}, `последнее_появление_в_сети` = '{now.strftime('%Y-%m-%d %H:%M:%S')}'")

        active_workers[device_msg["worker_id"]] = now
        conn.commit()

        if device_msg["code"] == 1:  # передача показаний
            params = device_msg["измерения"]  # массив кортежей раб, параметр, время, измерение само
            cur.executemany(f" insert into `журнал_показаний` values(%s, %s, %s, %s)", params)
            print(params)

            conn.commit()  # обязательно

        elif device_msg["code"] == 2:  # получить пороги и корректировки

            cur.execute(f"select название_параметра, код_параметра from параметры")
            device_params = {}
            for i in cur:
                device_params[i[0]] = i[1]
            answer["параметры"] = device_params
            cur.execute(f"select код_параметра, корректировка_нижнего_порога, корректировка_верхнего_порога from корректировки where табельный_номер = {device_msg['worker_id']}")

            correct = {}
            for i in cur:
                correct[i[0]] = i[1], i[2]
            answer["корректировки"] = correct
            cur.execute(f"select код_параметра ,нижний_допустимый_порог, верхний_допустимый_порог from допустимые_значения_параметров"
                        f" where код_категории_вредности in "
                        f"(SELECT код_категории_вредности from работники where табельный_номер = {device_msg['worker_id']})")  # получение порогов по категории
            porogs = {}
            for i in cur:
                porogs[i[0]] = i[1], i[2]
            answer["пороги"] = porogs

        elif device_msg["code"] == 10:  # закрытие смены
            cur.execute(f"delete from активные_рабочие where табельный_номер = {device_msg['worker_id']}")
            del active_workers[device_msg["worker_id"]]
            conn.commit()


        # now = datetime.datetime.now()
        # now.strftime('%Y-%m-%d %H:%M:%S')





        answer["messages"] = get_worker_msgs(device_msg['worker_id'])

        answer = json.dumps(answer)
        answer = answer.encode()
        self.request.sendall(answer)


if __name__ == "__main__":
    conn = mysql.connector.connect(host="localhost",
                                   user="cthulhudemon",
                                   passwd="1122",
                                   database="cthulhudb",
                                   use_pure=True)
    cur = conn.cursor()
    HOST, PORT = "", 9090

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

