from html.parser import HTMLParser
from re import sub
from html_sanitizer import Sanitizer
sanitizer = Sanitizer({'attributes': {}})

class MLRemover(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.reset()
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def handle_entityref(self, name):
        self.fed.append(f'&{name};')

    def handle_charref(self, name):
        self.fed.append(f'&#{name};')

    def get_data(self):
        return ''.join(self.fed)

def stripHtml(value):
    remover = MLRemover()

    remover.feed(value)
    remover.close()
    return remover.get_data()

def sanitizeHtml(html_text):
    return sanitizer.sanitize(html_text)

def textMarkDown(text):
    from markdownify import markdownify as md
    return md(text, strip=['a'])

def camelCase(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])

def nameNotation(text):
    notation = text.lower().replace(" ", "_")
    return notation
