from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class ScrapyNovatec:

    def __init__(self):
        self.base_url = "https://novatec.com.br/"
        self.url = ""
        pass

    def get_soap(self, url):
        self.url = url
        html = urlopen(url)
        soap_html = BeautifulSoup(html.read(), "html.parser")
        return soap_html

    def get_launch_books(self):
        soap_html = self.get_soap(url=self.base_url)
        soap_match = soap_html.find_all("tr", valign="center")
        books = []
        for e in soap_match:
            try:
                id_image = re.search(r'.+/(.+)\.gif', e.img['src']).group(1)
                books.append({"name": e.h1.text,
                              "image": self.base_url + e.a['href'] + '/capa_ampliada' + id_image + '.jpg',
                              "description": e.h2.text
                              })
            except:
                # shut up
                pass
        return books

    def get_next_launch(self):
        soap_html = self.get_soap(self.base_url)
        soap_match = soap_html.find_all("tr", valign="center", align="center")
        books = []
        for block in soap_match:
            for td in block.find_all("td"):
                try:
                    books.append({"name": td.img['alt'],
                                  "image": self.base_url+td.img['src']
                                  })
                except:
                    # shut up
                    pass

        return books

    def get_category(self):
        soap_html = self.get_soap(self.base_url)
        soap_match = soap_html.find_all("td", align="left")
        category = []
        for cat in soap_match:
            try:
                id_category = re.search(r'.+id=([0-9]+)', cat.a["href"]).group(1)
                category.append({"id": id_category,
                                 "title": cat.text
                                 })
            except:
                # shut up
                pass

        return category

    def get_by_category(self, id, page):

        soap_html = self.get_soap(url="https://novatec.com.br/lista.php?id="+id+"&pag="+page)
        books = []


        """
        //@Breno way, tem um pequeno bug duplicando o resultado
        blocks = soap_html.find_all('td')

        for block in blocks:
            if not block.find('a'):
                continue
            if not 'livros' in block.find('a').attrs['href']:
                continue

            simple_tags = block.findAll('a')

            #book_image = self.base_url+block.find("img", hspace="6")["src"]

            author = ''.join([a.text for a in simple_tags if 'autores' in a.attrs['href']])
            book_name = ''.join([a.text for a in simple_tags if 'livros' in a.attrs['href']])
            brs = block.find_all('br')
            if brs:
                year, pages, price = [b.split(':')[1].strip()
                        for b in brs[1].text.split('\n')
                        if b.strip() != ''
                ]
                book_image = block.find('img').attrs.get('src', '')

                books.append({"image":book_image,
                              "title": book_name,
                              "author": author,
                              "year": year,
                              "pages": pages,
                              "price": price
                              })
                #print({"autor": author, "name": book_name, "year": year, "pages": pages, "price": price})
                print(books)
    """
        for e in soap_html.findAll("tr"):
            try:
                year_pages_price_not_formatted_text = e.find(
                    "font", face="Arial", size="2").br.br.text.strip("\t\n\r ").split("\n")

                book_year = year_pages_price_not_formatted_text[0].split(":")[1].strip("\t\n\r ")
                book_pages = year_pages_price_not_formatted_text[2].split(":")[1].strip("\t\n\r ")
                book_price = year_pages_price_not_formatted_text[4].split(":")[1].strip("\t\n\r ")

                books.append({"image": self.base_url+e.a.find("img", hspace="6")["src"],
                              "title": e.find("font", face="Arial", size="2").a.text,
                              "author": e.find("font", face="Arial", size="2").br.a.text,
                              "year": book_year,
                              "pages": book_pages,
                              "price": book_price
                              })
            except:
                # shut up
                pass

        return books

