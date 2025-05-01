import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

# Configuração
rss_url = 'https://webterra.com.br/wp-json/wp/v2/posts?per_page=10&_embed'

# Gera feed
fg = FeedGenerator()
fg.load_extension('dc', 'content')
fg.title('WebTerra - Norte de Minas')
fg.link(href='https://webterra.com.br/categoria/norte-de-minas')
fg.description('Notícias do norte de Minas do WebTerra')
fg.language('pt-br')
fg.generator('python-feedgen')
fg.lastBuildDate(datetime.now(pytz.utc))

# Busca posts
response = requests.get(rss_url)
posts = response.json()

# Filtrar palavras proibidas
blacklist = ['morte', 'morre', 'acidente', 'vítima', 'vítimas', 'droga', 'drogas', 'maconha', 'polícia']
filtered_posts = [post for post in posts if not any(word in post['title']['rendered'].lower() for word in blacklist)]

for post in filtered_posts:
    title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
    link = post['link']
    description = BeautifulSoup(post['excerpt']['rendered'], 'html.parser').get_text()
    content = post['content']['rendered']
    soup = BeautifulSoup(content, 'html.parser')

    # Encontrar a maior imagem
    largest_img = ''
    largest_width = 0

    for img in soup.find_all('img'):
        if img.has_attr('srcset'):
            srcset_list = [s.strip().split(' ') for s in img['srcset'].split(',')]
            for src_item in srcset_list:
                if len(src_item) >= 2:
                    src, width = src_item
                    width_value = int(width.replace('w', '')) if 'w' in width else 0
                    if width_value > largest_width:
                        largest_img = src
                        largest_width = width_value
        elif img.has_attr('src') and not largest_img:
            largest_img = img['src']

    # Montar HTML com a melhor imagem + conteúdo completo
    content_html = ''
    if largest_img:
        content_html += f'<img src="{largest_img}" /><br>'
    content_html += str(soup)

    # Criar item do feed
    fe = fg.add_entry()
    fe.id(str(post['id']))
    fe.title(title)
    fe.link(href=link)
    fe.description(description)
    fe.pubDate(datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc))
    fe.content(content_html, type='CDATA')

# Salvar arquivo como v2_2
fg.rss_file('webterra_rss_v2_2.xml')
print("✅ XML gerado com sucesso: webterra_rss_v2_2.xml")
