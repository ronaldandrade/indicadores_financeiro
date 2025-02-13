import streamlit as st
import requests
from bs4 import BeautifulSoup

# Configuração da página
st.set_page_config(page_title="Notícias do Mercado", layout="wide")

st.title("📈 Últimas Notícias do Mercado Financeiro")

# URLs dos sites de notícias
urls = {
    "G1": "https://g1.globo.com/",
    "Folha": "https://www1.folha.uol.com.br/",
    "Yahoo Finanças": "https://br.financas.yahoo.com/",
    "InfoMoney": "https://www.infomoney.com.br/",
}

# Classes CSS para encontrar os links das notícias em cada site
classes = {
    "G1": "feed-post-link",
    "Folha": "c-headline__url",
    "Yahoo Finanças": "",
    "InfoMoney": "",
}

# Entrada de palavras-chave pelo usuário
user_input = st.text_input("🔍 Digite palavras-chave separadas por vírgula:", "china, mercado, dólar, governo, comércio, petróleo, brasil")
palavras_chave = [p.strip().lower() for p in user_input.split(",") if p.strip()]

# Função para buscar notícias
def buscar_noticias(site, url, classe_link, palavras_chave):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    noticias = soup.find_all("a", {"class": classe_link})

    lista_noticias = []
    for noticia in noticias:
        titulo = noticia.text.strip()
        link = noticia["href"]
        for palavra in palavras_chave:
            if palavra in titulo.lower():
                lista_noticias.append({"titulo": titulo, "link": link, "fonte": site})
                break  # Evita repetição da mesma notícia

    return lista_noticias

# Seleção das fontes de notícias
fontes_selecionadas = st.multiselect("📌 Escolha as fontes de notícias:", list(urls.keys()), default=list(urls.keys()))

# Buscar e exibir notícias
todas_noticias = []
for site in fontes_selecionadas:
    todas_noticias.extend(buscar_noticias(site, urls[site], classes[site], palavras_chave))

# Exibir notícias em formato de cards
st.subheader("📰 Resultados da Busca")
if todas_noticias:
    for noticia in todas_noticias:
        with st.container():
            st.markdown(f"**{noticia['titulo']}**")
            st.markdown(f"[🔗 Link para a notícia]({noticia['link']}) - *Fonte: {noticia['fonte']}*")
            st.write("---")
else:
    st.warning("Nenhuma notícia encontrada com as palavras-chave informadas.")
