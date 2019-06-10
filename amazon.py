# Recupera las ofertas de la página de Amazon.
# Usamos herramientas de manipulación de strings para no entrar en selenium.
# Al ser una web dinámica y descargarla sin que se ejecute JavaScrip, nos limita solo a
# 8 ofertas, aunqe se puedan recuperar más Ids
#
# EJEMPLO DE USO
#
# app = Amazon()
# data = app.get_data() #  diccionario de datos
# app.to_csv()  # genera un csv
#
# EJEMPLO RE SALIDA
#
# {
#  'e79a0334' : {
#         'egressUrl': 'https://www.amazon.es/dp/B01ETRGE7M',
#         'primeAccessDuration': '0',
#         'glProductGroup': 'gl_digital_devices_4',
#         'msToEnd': '207110396',
#         'reviewRating': '4.395130244',
#         'primaryImage': 'https://images-na.ssl-images-amazon.com/images/I/415kiMyoKpL.jpg',
#         'maxPercentOff': '25',
#         'msToStart': '-396789604',
#         'reviewAsin': 'B01ETRGE7M',
#         'minPrevPrice': '39.99',
#         'maxListPrice': '39.99',
#         'isMAP': '0',
#         'displayPriority': '0',
#         'isEligibleForFreeShipping': '0',
#         'isPrimeEligible': '1',
#         'dealID': 'e79a0334',
#         'description': 'Ahorra 10€ en Fire TV Stick',
#         '*className*': 'dcs.model.DealDetails',
#         'title': 'Ahorra 10€ en Fire TV Stick',
#         'type': 'BEST_DEAL',
#         'maxBAmount': '39.99',
#         'merchantName': 'Amazon.es',
#         'maxCurrentPrice': '29.99',
#         'impressionAsin': 'B01ETRGE7M',
#         'isFulfilledByAmazon': '0',
#         'maxDealPrice': '29.99',
#         'offerID': 'X5ZjOPB%2BAC1u8gwRPlYcXBeWT66QxCFxazdyZ4Mo4UZfsihRlytarHMP59NJF3nuQ%2BDDaUc8',
#         '*classHierarchy*': '[\n            dcs.model.DealDetails\n         ]',
#         'maxPrevPrice': '39.99',
#         'minBAmount': '39.99',
#         'currencyCode': 'EUR',
#         'minListPrice': '39.99',
#         'merchantID': 'A1AT7YVPFBWXBL',
#         'score': '0',
#         'bKind': 'ULP',
#         'msToFeatureEnd': '0',
#         'minCurrentPrice': '29.99',
#         'ingressUrl': 'https://www.amazon.es/gp/goldbox',
#         'isFeatured': '0',
#         'totalReviews': '8166',
#         'minDealPrice': '29.99',
#         'itemType': 'SINGLE_ITEM',
#         'minPercentOff': '25',
#         'items': '[\n\n         ]'
#     },
# '13afff4c' : { ... },
# ....
# }

import requests
import file_handle


class Amazon(file_handle.FileHandle):
    def __init__(self):
        self.DEAL_ID = 'sortedDealIDs'
        self.DEAL_DETAIL = 'dealDetails'
        self.END = 'responseMetadata'
        self.url = 'https://www.amazon.es/gp/goldbox/?ref_=nav_cs_npx_todaysdeals'
        self.file_name = 'amazon'
        self.url_text = self._get_url_data()
        super(Amazon, self).__init__(self.file_name)

    def get_data(self):
        """
        Recupera datos de Ids y texto a buscar y devuelve un diccionario con los datos finales
        :return: dict
        """
        ids = self._find_ids()
        new_text = self._text_deals()
        return self._generate_data(new_text, ids)

    def _generate_data(self, deals, ids):
        """
        Recoge los datos finales y los devuelve en un diccionario
        Reestructuración del diccionario para una mejor visión y acceso
        :param deals: dict, diccionario con los datos en bruto
        :param ids: list, listado de las ids de las ofertas
        :return: dict, diccionario reestructurado para mejor acceso
        """
        dic = {}
        for item in ids:
            dic[item] = self._find_deals(deals, item)
        return dic

    def _get_url_data(self):
        """
        Recupera los datos en formato texto de la web
        :return: string
        """
        return requests.get(self.url).text

    def _find_ids(self):
        """
        Bisca las ids en el texto
        :return: list
        """
        text = self._cut_text(self.url_text, self.DEAL_ID,  '[', ']')
        cleaned = self._clean_text(text)
        return cleaned[:8]

    def _clean_text(self, text):
        """
        Limpia espacios y finales de linea del texto
        :param text: string
        :return: list
        """
        text = text.replace('"', '')
        text = text.split(',')
        return [item.strip() for item in text]

    def _cut_text(self, text, begin, strt='{', stp='}'):
        """
        Corta el texto con los datos de inicio y fin indicados
        :param text: string, texto a cortar
        :param begin: string, punto de partida a cortar
        :param ini: string, simbolo de inicio
        :param fin: string, simbolo fin
        :return: string, texto cortado
        """
        base = text.find(begin)
        new_text = text[base:]
        start = new_text.find(strt) + 1
        stop = new_text.find(stp)
        return new_text[start:stop]

    def _text_deals(self):
        """
        Recorta el texto que contiene los datos de todos los deals
        :return: string
        """
        text_start = self.url_text.find(self.DEAL_DETAIL)
        text_stop = self.url_text.find(self.END)
        return self.url_text[text_start:text_stop]

    def _find_deals(self, text, inicio):
        """
        Una vez recortado y limpiado el texto, generamos una lista de listas. Cada lista se separa en dos valores.
        Con esa lista generamos un diccionario.

        :param text: string, texto de busqueda
        :param inicio: string, cadena de inicio de busquesda
        :param be: string, simbolo deinicio de busqueda
        :param en: string, simbolo de fin de busqueda
        :return: dict, diccionario con datos en bruto.
        """
        text = self._cut_text(text, inicio)
        new_text = self._clean_text(text)
        text_list = [element.split(' : ') for element in new_text]
        new_list = [item for item in text_list if len(item) == 2]

        dic = dict((key, value) for key, value in new_list)

        return dic

    def to_csv(self):
        """
        Crea un archivo csv con los datos.
        Producto, Precio, Url, Imagen
        """
        data = self.get_data()
        new_data = self._prepare_data(data)
        self._file_write(new_data)

    def _prepare_data(self, data):
        """
        Recupera los datos en formato lista y los devuelve como diccionario con las keys
        title, minDealPrice, egressUrl, primaryImage
        :param data: list
        :return: dict
        """
        list_data = []
        for item in data.keys():
            list_data.append([
                data[item].get('title'),
                data[item].get('minDealPrice'),
                data[item].get('egressUrl'),
                data[item].get('primaryImage')
            ])
        return list_data


if __name__ == '__main__':

    app = Amazon()
    print(app.get_data())
    app.to_csv()


