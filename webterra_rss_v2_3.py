import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

rss_url = 'https://webterra.com.br/wp-json/wp/v2/posts?per_page=10&_embed'

fg = FeedGenerator()
fg.load_extension('dc', 'content')
fg.title('WebTerra - Norte de Minas')
fg.link(href='https://webterra.com.br/categoria/norte-de-minas')
fg.description('Notícias do norte de Minas do WebTerra')
fg.language('pt-br')
fg.generator('python-feedgen')
fg.lastBuildDate(datetime.now(pytz.utc))

blacklist = ['morte', 'morre', 'acidente', 'vítima', 'vítimas', 'droga', 'drogas', 'maconha', 'polícia']

response = requests.get(rss_url)
posts = response.json()

for post in posts:
    title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
    if any(word in title.lower() for word in blacklist):
        continue

    link = post['link']
    description = BeautifulSoup(post['excerpt']['rendered'], 'html.parser').get_text()
    content = post['content']['rendered']
    soup = BeautifulSoup(content, 'html.parser')

    # Busca imagem pela classe específica
    img_tag = soup.find('img', class_='attachment-pixwell_780x0-2x size-pixwell_780x0-2x wp-post-image')
    img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''

    if img_url:
        content_html = f'<img src="{img_url}" /><br>{str(soup)}'
        description_html = f'<img src="{img_url}" /> {description}'
    else:
        content_html = str(soup)
        description_html = description

    fe = fg.add_entry()
    fe.id(str(post['id']))
    fe.title(title)
    fe.link(href=link)
    fe.description(description_html)
    fe.pubDate(datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc))
    fe.content(content_html, type='CDATA')

fg.rss_file('webterra_rss_v2_3.xml')
print("✅ XML gerado com sucesso: webterra_rss_v2_3.xml")
