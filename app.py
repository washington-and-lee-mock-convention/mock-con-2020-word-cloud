import requests
from html2text import html2text

def main():
    html = requests.get('https://www.nytimes.com/2019/09/20/us/politics/trump-whistle-blower-ukraine.html')
    text = html2text(html.text)
    print(text)

if __name__ == '__main__':
    main()
