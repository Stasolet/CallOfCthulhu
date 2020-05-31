import mysql.connector
import datetime
import math

conn = None
cur = None


def generate(worker_id, mouth, day, start_hour=8, end_hour=16, year=2020):

    morn = datetime.datetime(year, mouth, day, start_hour)
    evn = datetime.datetime(year, mouth, day, end_hour)
    freq = datetime.timedelta(seconds=4)
    moment = morn + freq
    values = [80, 50, 30, 36.6]
    params = []
    while moment < evn:
        for param_id, val in enumerate(values, 1):
            if param_id == 1:
                val = val + 10 * math.sin(moment.second/10)
            params.append((worker_id, param_id, moment.strftime('%Y-%m-%d %H:%M:%S'), val))
        moment = moment + freq

    cur.executemany(f" insert into `журнал_показаний` values(%s, %s, %s, %s)", params)

    conn.commit()




if __name__ == "__main__":
    conn = mysql.connector.connect(host="localhost",
                                   user="cthulhudemon",
                                   passwd="1122",
                                   database="cthulhudb",
                                   use_pure=True)

    cur = conn.cursor()
    for i in range(2, 30):
        generate(1, 5, i)

