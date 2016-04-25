from urllib.request import urlopen
from bs4 import BeautifulSoup
from book import Book

class Scrapy_novatec:
    def __init__(self):
        self.base_url = "https://novatec.com.br/"
        self.url =""
        pass

    def getSoap(self, url):
        self.url = url
        html = urlopen(url)
        soap_html = BeautifulSoup(html.read(), "html.parser")
        return soap_html

    def getLancamentoBooks(self):
        """
        retorna uma lista de livros
        referente ao lancamento
        :return:
        """
        soap_html = self.getSoap(url=self.base_url)
        soap_match = soap_html.find_all("tr", valign="center")
        books =[]
        for e in soap_match:
            try:
                book = Book(name=e.h1.text,
                            image=self.base_url+e.img['src'],
                            description=e.h2.text
                            )
                books.append(book)
            except:
                #esse Pog e pq o site e uma bosta
                #foi preciso ignorar alguns resultados
                pass
        return books

    def getEmBreve(self):
        """
        Retorna uma lista de livros
        referente aos proximos lancamentos
        :return:
        """
        soap_html = self.getSoap(self.base_url)
        soap_match = soap_html.find_all("tr", valign="center", align="center")
        books = []
        for block in soap_match:
            for td in block.find_all("td"):
                try:
                    book = Book(name=td.img['alt'],
                                image=self.base_url+td.img['src'],
                                description="")
                    books.append(book)
                except:
                    #bug no parser
                    pass

        return books

    def getByCategory(self):
        soap_html = self.getSoap(url="https://novatec.com.br/lista.php?id=28")
        books = []
        for e in soap_html.findAll("tr"):
            try:
                complex_pog = e.find("font", face="Arial", size="2").br.br.text.strip("\t\n\r ").split("\n")
                print (complex_pog[0].split(":")[1])

                books.append({"image": self.base_url+e.a.find("img", hspace="6")["src"],
                              "title": e.find("font", face="Arial", size="2").a.text,
                              "author": e.find("font", face="Arial", size="2").br.a.text,
                              "ano": complex_pog[0].split(":")[1].strip("\t\n\r "),
                              "paginas": complex_pog[2].split(":")[1].strip("\t\n\r "),
                              "preco": complex_pog[4].split(":")[1].strip("\t\n\r ")
                              })
            except:
                pass
        return books
if __name__ == '__main__':
    c = Scrapy_novatec()
    c.getByCategory()
