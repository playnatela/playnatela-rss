import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

# Configuração
rss_url = 'https://webterra.com.br/wp-json/wp/v2/posts?per_page=20&_embed'

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
blacklist = [
    'morte', 'morre', 'acidente', 'vítima', 'vítimas', 'droga', 'drogas',
    'maconha', 'polícia', 'furto', 'preso', 'presa', 'webterra',
    'homicídio', 'homicidios', 'assassinato', 'assassinatos',
    'latrocínio', 'latrocinios', 'estupro', 'estupros',
    'agressão', 'agressoes', 'agredido', 'agredida', 'ameaça', 'ameaças',
    'tiroteio', 'tiroteios', 'facada', 'facadas', 'arma', 'armas',
    'baleado', 'baleada', 'baleados', 'baleadas',
    'facão', 'facões', 'incêndio', 'incêndios', 'sequestro', 'sequestros',
    'desaparecido', 'desaparecida', 'desaparecidos', 'desaparecidas'
]

filtered_posts = [post for post in posts if not any(word in post['title']['rendered'].lower() for word in blacklist)]

for post in filtered_posts:
    title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
    link = post['link']
    description = BeautifulSoup(post['excerpt']['rendered'], 'html.parser').get_text()
    content = post['content']['rendered']
    soup = BeautifulSoup(content, 'html.parser')

    # Inicializa a imagem principal
    main_img_url = ''

    # Tenta pegar diretamente do conteúdo, filtrando por domínio webterra.com.br
    img_urls = []
    for img in soup.find_all('img'):
        if img.has_attr('srcset'):
            srcset = img['srcset'].split(',')
            largest_img = srcset[-1].strip().split(' ')[0]
            if 'webterra.com.br' in largest_img:
                img_urls.append(largest_img)
        elif img.has_attr('src'):
            if 'webterra.com.br' in img['src']:
                img_urls.append(img['src'])

    if img_urls:
        main_img_url = img_urls[0]
    else:
        # Busca a imagem destacada na página do artigo (com filtro de domínio)
        try:
            page_response = requests.get(link, timeout=5)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            highlight_img = page_soup.find('img', class_='attachment-pixwell_780x0-2x')
            if highlight_img and highlight_img.has_attr('src'):
                if 'webterra.com.br' in highlight_img['src']:
                    main_img_url = highlight_img['src']
        except Exception as e:
            print(f"⚠ Erro ao buscar imagem destacada de {link}: {e}")

    # Montar HTML com imagem principal + conteúdo
    content_html = ''
    if main_img_url:
        content_html += f'<img src="{main_img_url}" /><br>'
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
fg.rss_file('webterra_rss_v2_4.xml')
print("✅ XML gerado com sucesso: webterra_rss_v2_4.xml")
