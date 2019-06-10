import csv
import os
from datetime import datetime


class FileHandle():
    def __init__(self, file):
        self._BASEDIR = os.path.dirname(__file__)
        self._CSV_DIR = os.path.join(self._BASEDIR, 'csv')
        self._file = file
        self._file_name = '{date}_{file}.csv'.format(
            date=datetime.today().strftime('%Y-%m-%d'),
            file=self._file
        )
        self._file_base = os.path.join(self._CSV_DIR, self._file_name)

    def _file_read(self):
        """
        Lee los datos de un csv. Utilizado para pruebas
        :return: list, lista de datos
        """
        result = []
        with open(self._file_base, 'r') as f:
            for line in enumerate(f):
                result.append(line[1])
        return result

    def _file_write(self, datas):
        """
        Escribe datos en un archivo csv
        datas: list, lista de datos a escribir
        """
        with open(self._file_base, 'w+') as f:

            writer = csv.writer(f)

            for data in datas:
                writer.writerow(data)
