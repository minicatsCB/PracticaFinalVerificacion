from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

parser = MyHTMLParser()
with urllib.request.urlopen('http://www.20minutos.es/noticia/3045391/0/luz-verde-remodelacion-bernabeu-entorno-con-dudas-juridicas-cs-psoe-con-hotel-pospuesto-otras-fases/') as f:
    b = f.read(300)

print(b)
parser.feed(str(b));