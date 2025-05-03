# PlayNaTela RSS

Este projeto exibe as últimas notícias do site WebTerra no formato de um visor automático para telas (digital signage).

## Funcionalidades

* Busca notícias do WebTerra usando a API WordPress.
* Filtra manchetes indesejadas por palavras-chave.
* Ignora imagens pequenas ou irrelevantes no destaque.
* Gera automaticamente um feed RSS (`webterra_rss_v2_4.xml`).
* Exibe as notícias com imagem de destaque, moldura e logo no visor HTML (`index_v2_4.html`).
* Atualiza o RSS automaticamente via GitHub Actions 3x por dia (03:00, 12:00 e 19:00 BRT).
* Valida o RSS gerado com `xmllint` no workflow.
* Notifica no GitHub em caso de falha (configure seus alertas no GitHub).

## Estrutura do repositório

* `.github/workflows/` → Workflow do GitHub Actions.
* `.gitignore` → Arquivos ignorados no repositório.
* `LOGO-WT.webp` → Logo do WebTerra.
* `moldura.png` → Moldura da tela.
* `index_v2_4.html` → Página HTML que exibe o feed.
* `requirements.txt` → Dependências Python.
* `webterra_rss_v2_4.py` → Script Python para gerar o RSS.
* `webterra_rss_v2_4.xml` → Arquivo RSS gerado.

## Como rodar localmente

1. Clone o repositório:

   ```bash
   git clone https://github.com/playnatela/playnatela-rss.git
   cd playnatela-rss
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o script para gerar o RSS:

   ```bash
   python webterra_rss_v2_4.py
   ```

4. Abra o arquivo `index_v2_4.html` no navegador.

## Automatização

O repositório usa GitHub Actions para rodar o script automaticamente às:

* 03:00 BRT
* 12:00 BRT
* 19:00 BRT

Você também pode rodar manualmente em:
[Actions → update-rss → Run workflow](https://github.com/playnatela/playnatela-rss/actions)

## Palavras filtradas (blacklist)

```text
morte, morre, acidente, vítima, vítimas, droga, drogas, maconha, polícia, 
furto, preso, presa, webterra, homicídio, homicidios, assassinato, assassinatos, 
latrocínio, latrocinios, estupro, estupros, agressão, agressoes, agredido, agredida, 
ameaça, ameaças, tiroteio, tiroteios, facada, facadas, arma, armas, 
baleado, baleada, baleados, baleadas, facão, facões, incêndio, incêndios, 
sequestro, sequestros, desaparecido, desaparecida, desaparecidos, desaparecidas
```

## Créditos

* Notícias: [WebTerra](https://webterra.com.br)
* Projeto: PlayNaTela

---

**Siga o projeto e deixe uma estrela! ⭐**

