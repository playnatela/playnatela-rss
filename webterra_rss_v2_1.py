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

    # Extrair todas as imagens (com alta resolução no srcset)
    img_urls = []
    for img in soup.find_all('img'):
        if img.has_attr('srcset'):
            # Pega a última (geralmente a maior) do srcset
            srcset = img['srcset'].split(',')
            largest_img = srcset[-1].strip().split(' ')[0]
            img_urls.append(largest_img)
        elif img.has_attr('src'):
            img_urls.append(img['src'])

    # Montar HTML com imagens + texto
    content_html = ''
    for img_url in img_urls:
        content_html += f'<img src="{img_url}" /><br>'
    content_html += str(soup)

    # Criar item do feed
    fe = fg.add_entry()
    fe.id(str(post['id']))
    fe.title(title)
    fe.link(href=link)
    fe.description(description)
    fe.pubDate(datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc))
    fe.content(content_html, type='CDATA')

# Salvar arquivo
fg.rss_file('webterra_rss_v2_1.xml')
print("✅ XML gerado com sucesso: webterra_rss_v2_1.xml")
