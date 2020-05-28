import mysql.connector
from PyQt5.QtWidgets import QErrorMessage


class DbWrapper:
    """Убогая реализация шаблона одиночки для доступа к базе данных"""
    __conn = None

    @staticmethod
    def connect(**kwargs):
        DbWrapper.__conn = mysql.connector.connect(**kwargs)

    @staticmethod
    def execute(operation: str, params=(), multi=False):  # Смотри что оборачиваешь, и его параметры
        """Функция не реализующая коннект по требованию и создание уникального курсора для каждого запроса"""
        try:
            cur = DbWrapper.__conn.cursor()
            cur.execute(operation, params, multi)
            return cur
        except Exception as err:
            error_widget = QErrorMessage()
            error_widget.showMessage(str(err))
            error_widget.exec()
            return None

    @staticmethod
    def callproc(procname: str, arg: tuple):
        cur = DbWrapper.__conn.cursor()
        cur.callproc(procname, arg)
        return cur

    @staticmethod
    def executemany(operation, seq_of_param):
        cur = DbWrapper.__conn.cursor()
        cur.executemany(operation, seq_of_param)
        return cur

    @staticmethod
    def commit():
        DbWrapper.__conn.commit()


db_wrapper = DbWrapper  # для соответствия стиля наименования python, потому что используется как объект, а не класс


