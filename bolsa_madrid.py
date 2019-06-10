# Recupera los datos de las acciones en la web web bolsamadrid.es.
#
# EJEMPLO DE USO
#
# app = BolsaMadrid()
# data = app.get_data() #  diccionario de datos
# app.to_csv()  # genera un csv
#
# EJEMPLO SALIDA
# {
#     '0':
#         {
#             'nombre': 'ACCIONA',
#             'ult': '100,5000',
#             'dif': '-1,57',
#             'max': '102,5000',
#             'min': '100,0000',
#             'volumen': '59.253',
#             'efectivo': '5.958,24',
#             'fecha': '10/06/2019',
#             'hora': '17:35'},
#     '1': {
#             'nombre': 'ACERINOX',
#             ...
#          }
#     .....
# }

import file_handle
import requests
from bs4 import BeautifulSoup


class BolsaMadrid(file_handle.FileHandle):
    def __init__(self):
        self.url = 'http://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000'
        self.keys = ['nombre', 'ult', 'dif', 'max', 'min', 'volumen', 'efectivo', 'fecha', 'hora']
        self.file_name = 'bolsa_madrid'
        self.url_text = self._get_url_data()
        super(BolsaMadrid, self).__init__(self.file_name)

    def _get_url_data(self):
        return requests.get(self.url).text

    def _generate_data(self):
        soup = BeautifulSoup(self.url_text, 'lxml')
        data = soup.find('table', attrs={'id': 'ctl00_Contenido_tblAcciones'})

        table = []
        for num, fila in enumerate(data.find_all('tr')):
            if num == 0:
                continue
            col = fila.find_all('td')
            coltab = []
            for celda in (col):
                coltab.append(celda.text)
            table.append(coltab)

        return table

    def _generate_dict(self, data):
        dic = {}
        for num, item in enumerate(data):
            dic[str(num)] = {
                self.keys[0]: item[0],
                self.keys[1]: item[1],
                self.keys[2]: item[2],
                self.keys[3]: item[3],
                self.keys[4]: item[4],
                self.keys[5]: item[5],
                self.keys[6]: item[6],
                self.keys[7]: item[7],
                self.keys[8]: item[8] if len(item) == 9 else ''  # puede estar suspendido
            }
        return dic

    def get_data(self):
        data = self._generate_data()
        return self._generate_dict(data)

    def to_csv(self):
        data = self._generate_data()
        self._file_write(data)


if __name__ == '__main__':
    app = BolsaMadrid()
    print(app.get_data())
    app.to_csv()