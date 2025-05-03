```markdown
# WebTerra RSS Automation

Este repositório gera e publica automaticamente um feed RSS atualizado para o portal [WebTerra](https://webterra.com.br), garantindo a entrega de notícias relevantes e sem conteúdos sensíveis.

---

## ⚙️ Funcionalidades principais

✅ Busca automática das últimas 20 notícias do WebTerra  
✅ Filtragem por blacklist para remover notícias de crimes, violência e tragédias  
✅ Seleção automática da melhor imagem disponível (ignorando imagens de 1x1 px ou placeholders)  
✅ Geração do arquivo `webterra_rss_v2_4.xml`  
✅ Validação automática do XML com `xmllint`  
✅ Commits automáticos com data/hora no formato:
```

🔄 Atualização automática do RSS (YYYY-MM-DD HH\:mm)

```
✅ Atualizações agendadas 3x ao dia:
- 03:00 UTC (00:00 BRT)
- 12:00 UTC (09:00 BRT)
- 19:00 UTC (16:00 BRT)

✅ Notificações por e-mail e no GitHub em caso de falha no workflow

---

## 📋 Blacklist atual

A blacklist remove notícias com estas palavras (incluindo variações):

```

'morte', 'morre', 'acidente', 'vítima', 'vítimas', 'droga', 'drogas', 'maconha',
'polícia', 'furto', 'preso', 'presa', 'homicídio', 'homicidios', 'assassinato',
'assassinatos', 'latrocínio', 'latrocinios', 'estupro', 'estupros', 'agressão',
'agressoes', 'agredido', 'agredida', 'ameaça', 'ameaças', 'tiroteio',
'tiroteios', 'facada', 'facadas', 'arma', 'armas', 'baleado', 'baleada',
'baleados', 'baleadas', 'facão', 'facões', 'incêndio', 'incêndios',
'sequestro', 'sequestros', 'desaparecido', 'desaparecida', 'desaparecidos',
'desaparecidas', 'webterra'

```

---

## 🏗️ Como funciona

1. O script Python (`webterra_rss_v2_4.py`) coleta e filtra as notícias.
2. Ele seleciona a imagem principal ignorando imagens mínimas.
3. Gera o arquivo XML.
4. Valida o XML usando `xmllint` no GitHub Actions.
5. Faz commit e push automático.
6. Em caso de falha, o GitHub envia e-mail para os responsáveis.

---

## 📦 Requisitos

- `requests`
- `beautifulsoup4`
- `feedgen`
- `pytz`

Instalação:
```

pip install -r requirements.txt

```

---

## 🔔 Notificações

Para receber alertas por e-mail:
- Vá para [GitHub Notifications Settings](https://github.com/settings/notifications)
- Marque as opções **On GitHub** e **Email** para workflows e falhas no repositório

