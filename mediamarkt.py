# Recuperamos las ofertas de la página principal de Mediamarkt
# Es uns página que monta las ofertas con JavaScript y html
# Para no usar selenium (por ahora, y como ejercicio),
# recuperamos los enlaces de las ofertas y los vamos visitando uno a uno
# para recuperar los datos de cada oferta.
# Es efectivo, pero, obviamente, mucho mas lento
#
#
# EJEMPLO DE USO
#
# app = Mediamarkt()
# data = app.get_data() #  diccionario de datos
# app.to_csv()  # genera un csv
#
# EJEMPLO DE SALIDA
# {'0':
#      {
#          'product': 'Aire acondicionado - LG 32EFI12WF.SET, Gas R32, Wi-Fi, Blanco',
#          'price': '599',
#          'image': 'picscdn.redblue.de/doi/pixelboxx-mss...',
#          'url': 'https://www.mediamarkt.es/es/product/_aire-....'
#      },
#  '1': {'product': 'Aur..',
#         .....}
#   ......
# }


import file_handle
import requests
from bs4 import BeautifulSoup


class Mediamarkt(file_handle.FileHandle):
    def __init__(self):
        self.url = 'https://www.mediamarkt.es/'
        self.file = 'mediamarkt'
        self.text = self._get_url_data()
        super(Mediamarkt, self).__init__(self.file)

    def _get_url_data(self):
        """
        Recuperamos los datos en formato texto de la url indicada
        :return: string
        """
        return requests.get(self.url).text

    def _get_links(self):
        """
        Recuperamos los enlaces de las ofertas
        """
        soup = BeautifulSoup(self.text, 'html.parser')
        area = soup.find_all('area', href=True, attrs={'shape': 'rect'})
        links = [links.get('href') for links in area]
        link = [link for link in links if 'product' in link]
        link = sorted(set(link))

        return link
    
    def _put_data(self):
        """
        Comprueba si ya existe un archivo con datos y si es así lo lee y devuelve los datos,
        Si no existe, recoge las urls y va etrando para construir los datos
        :return: list
        """
        list_links = []
        links = self._get_links()
        tot = len(links)
        for num, item in enumerate(links):
            print("{0:2.0f}%".format(num/tot*100))
            product_url = item
            product = requests.get(product_url).text
            s_product = BeautifulSoup(product, 'lxml')
            p_name = s_product.find('h1', attrs={'itemprop': 'name'})
            p_price = s_product.find('div', attrs={'class': 'price'})
            p_image = s_product.find('img', attrs={'class': 'img-preview'})
            if p_name is not None and p_price is not None and p_image is not None:
                name = p_name.contents[0]
                price = p_price.contents[0] if not p_price.contents[0].endswith(',-') else p_price.contents[0][:-2]
                image = p_image.get('src')[2:]
                list_links.append([name, price, image, item])

        return list_links

    def get_data(self):
        """
        Recupera los datos en formato lista y los devuelve como diccionario
        :return: dict
        """

        data = self._put_data()
        dic = {}
        for num, item in enumerate(data):

            dic[str(num)] = {
                'product': item[0],
                'price': item[1],
                'image': item[2],
                'url': item[3]
            }
        return dic

    def to_csv(self):
        """
        Recupera los datos y los envía al metodo _file_write para crear un csv

        """
        links = self._put_data()
        self._file_write(links)


if __name__ == '__main__':
    app = Mediamarkt()
    # app.to_csv()
    pp = app.get_data()

