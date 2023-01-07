from html.parser import HTMLParser
import requests


class ParserRusplitka(HTMLParser):
    res = {}
    price = []

    def handle_starttag(self, tag, attrs):
        self.res['attrs'] = attrs
        for x in self.res['attrs']:
            if x == ('itemprop', 'price'):
                self.price.append({
                    'price': self.res['attrs'][-1][1],
                })


url = 'https://samara.rusplitka.ru/catalog/klinkernaya-plitka/'
response = requests.get(url=url)

with open('page.html', 'w') as file:
    file.write(response.text)

with open('page.html', 'r') as file:
    page = file.read()


parser = ParserRusplitka()
parser.feed(page)
print(parser.price)

