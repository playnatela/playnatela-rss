Aqui está um modelo pronto de README.md para seu repositório playnatela-rss no GitHub:

# PlayNaTela RSS

Este projeto exibe as últimas notícias do site WebTerra no formato de um visor automático para telas (digital signage).

## Funcionalidades

- Busca notícias do WebTerra usando a API WordPress.
- Filtra manchetes indesejadas por palavras-chave.
- Gera automaticamente um feed RSS (`webterra_rss_v2_4.xml`).
- Exibe as notícias com imagem de destaque em um visor HTML (`index_v2_4.html`).
- Atualiza o RSS automaticamente via GitHub Actions 2x por dia (00:00 e 12:00 BRT).

## Estrutura do repositório

- `.github/workflows/` → Contém o workflow do GitHub Actions.
- `.gitignore` → Arquivos a serem ignorados no repositório.
- `LOGO-WT.webp` → Logo do WebTerra.
- `moldura.png` → Moldura da tela.
- `index_v2_4.html` → Página HTML que exibe o feed.
- `requirements.txt` → Dependências Python.
- `webterra_rss_v2_4.py` → Script Python para gerar o RSS.
- `webterra_rss_v2_4.xml` → Arquivo RSS gerado.

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

O repositório está configurado com GitHub Actions para rodar o script automaticamente às:
- 00:00 BRT
- 12:00 BRT

Além disso, é possível rodar manualmente em [Actions → update-rss → Run workflow](https://github.com/playnatela/playnatela-rss/actions).

## Créditos

- Notícias: [WebTerra](https://webterra.com.br)
- Projeto: PlayNaTela

---

**Siga o projeto e deixe uma estrela!**

Se quiser, posso já gerar o arquivo .md pronto pra você subir no repositório. Quer?
