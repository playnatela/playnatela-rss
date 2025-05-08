import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
from dateutil import parser

# Configuração
rss_url = 'https://webterra.com.br/wp-json/wp/v2/posts?per_page=20&_embed'
headers = {'User-Agent': 'Mozilla/5.0'}

# Função segura para parse de data
def safe_parse_date(date_str):
    try:
        return parser.parse(date_str)
    except Exception:
        return datetime(1970, 1, 1)

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
response = requests.get(rss_url, headers=headers, timeout=10)
if response.status_code != 200:
    print(f"❌ Erro ao acessar API: {response.status_code}")
    exit()
posts = response.json()

# Ordenar por data decrescente usando safe_parse_date
posts.sort(key=lambda x: safe_parse_date(x.get('date', '1970-01-01')), reverse=True)

# Blacklist de palavras
blacklist = [
    'morte', 'morre', 'acidente', 'vítima', 'vítimas', 'droga', 'drogas',
    'maconha', 'polícia', 'furto', 'preso', 'presa', 'webterra',
    'homicídio', 'homicidios', 'assassinato', 'assassinatos',
    'latrocínio', 'latrocinios', 'estupro', 'estupros',
    'agressão', 'agressoes', 'agredido', 'agredida', 'ameaça', 'ameaças',
    'tiroteio', 'tiroteios', 'facada', 'facadas', 'arma', 'armas',
    'baleado', 'baleada', 'baleados', 'baleadas',
    'facão', 'facões', 'incêndio', 'incêndios', 'sequestro', 'sequestros',
    'desaparecido', 'desaparecida', 'desaparecidos', 'desaparecidas',
    'receita', 'sobremesa', 'culinária', 'culinaria', 'reflexão', 'poesia',
    'opinião', 'opinião', 'crônica', 'cronica', 'coluna', 'ingrediente', 'ingredientes'
]

# Função para verificar se contém palavra proibida
def contains_blacklisted_word(text):
    text_lower = text.lower()
    return any(word in text_lower for word in blacklist)

# Filtrar posts
filtered_posts = []
for post in posts:
    title = BeautifulSoup(post.get('title', {}).get('rendered', ''), 'html.parser').get_text()
    excerpt = BeautifulSoup(post.get('excerpt', {}).get('rendered', ''), 'html.parser').get_text()
    content = BeautifulSoup(post.get('content', {}).get('rendered', ''), 'html.parser').get_text()

    combined_text = f"{title} {excerpt} {content}"

    if not contains_blacklisted_word(combined_text):
        filtered_posts.append(post)

# Ordenar novamente após filtro
filtered_posts.sort(key=lambda x: safe_parse_date(x.get('date', '1970-01-01')), reverse=True)

for post in filtered_posts:
    title_html = post.get('title', {}).get('rendered', '')
    link = post.get('link', '')
    description_html = post.get('excerpt', {}).get('rendered', '')
    content_html = post.get('content', {}).get('rendered', '')
    date_str = post.get('date', '')

    title = BeautifulSoup(title_html, 'html.parser').get_text()
    description = BeautifulSoup(description_html, 'html.parser').get_text()
    soup = BeautifulSoup(content_html, 'html.parser')

    # Inicializa a imagem principal
    main_img_url = ''
    img_urls = []

    for img in soup.find_all('img'):
        if img.has_attr('srcset'):
            srcset = img['srcset'].split(',')
            largest_img = srcset[-1].strip().split(' ')[0]
            if 'webterra.com.br' in largest_img:
                img_urls.append(largest_img)
        elif img.has_attr('src') and 'webterra.com.br' in img['src']:
            img_urls.append(img['src'])

    if img_urls:
        main_img_url = img_urls[0]
    else:
        try:
            page_response = requests.get(link, headers=headers, timeout=10)
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                highlight_img = page_soup.find('img', class_='attachment-pixwell_780x0-2x')
                if highlight_img and highlight_img.has_attr('src') and 'webterra.com.br' in highlight_img['src']:
                    main_img_url = highlight_img['src']
        except Exception as e:
            print(f"⚠ Erro ao buscar imagem destacada de {link}: {e}")

    entry_content = ''
    if main_img_url:
        entry_content += f'<img src="{main_img_url}" /><br>'
    entry_content += str(soup)

    fe = fg.add_entry()
    fe.id(str(post.get('id', '')))
    fe.title(title)
    fe.link(href=link)
    fe.description(description)
    try:
        pub_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
    except Exception:
        pub_date = datetime.now(pytz.utc)
    fe.pubDate(pub_date)
    fe.content(entry_content, type='CDATA')

# Salvar arquivo
fg.rss_file('webterra_rss_v2_4.xml')
print("✅ XML gerado com sucesso: webterra_rss_v2_4.xml")
