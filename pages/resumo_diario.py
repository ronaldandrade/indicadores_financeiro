import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from utils.top_day import GetTopGainers, GetTopLosers, topGainers
# from utils.btc_day import exibir_valores

def configurar_pagina():
    """
    Configura a página inicial do Streamlit com layout 'wide'.
    """
    st.set_page_config(
    page_title="Resumo Diário",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)
    st.title('IBOVESPA')
    
def obter_dados_indice(ticker, periodo="6mo"):
    """
    Baixa os dados históricos de um índice usando yfinance.
    
    Args:
    - ticker (str): O símbolo do índice (e.g., '^IXIC' para NASDAQ).
    - periodo (str): O período de tempo para o qual baixar os dados. Exemplo: '6mo'.
    
    Returns:
    - pd.DataFrame: DataFrame contendo os dados históricos.
    """
    dados = yf.Ticker(ticker).history(period=periodo)
    return dados

def calcular_variacao(dados):
    """
    Calcula a variação percentual entre o fechamento do dia anterior e o fechamento mais recente.
    
    Args:
    - dados (pd.DataFrame): DataFrame contendo os dados históricos do índice ou moeda.
    
    Returns:
    - close (float): O valor de fechamento mais recente.
    - variacao (float): A variação percentual entre o dia anterior e o fechamento mais recente.
    """
    close = dados['Close'].iloc[-1]
    dia_anterior = dados['Close'].iloc[-2]
    variacao = ((close - dia_anterior) / dia_anterior) * 100
    return close, round(variacao, 2)

def gerar_grafico(dados_ibovespa):
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')
        ax.plot(dados_ibovespa.index, dados_ibovespa['Close'], color='skyblue')
        ax.set_xlim(dados_ibovespa.index[0], dados_ibovespa.index[-1])
        ax.set_ylim(dados_ibovespa['Close'].min(), dados_ibovespa['Close'].max())
        ax.set_xticks(dados_ibovespa.index[::15])
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig, transparent=True)
        return

def gerar_relatorio(top_gainers, top_losers):
        """
        Estrutura de apresentação do relatório de maiores altas e baixas do dia
        
        Args:
            (top_gainers, top_losers): as maiores altas e maiores baixas respectivamente 
        até o momento de atualizaçao da página.


        """
        col1, col2 = st.columns(2)
        
        # Exibição das Maiores Altas
        with col1:
            st.subheader("Maiores Altas")
            for ticker, price in zip(top_gainers.topGainersDay['tickers'], top_gainers.topGainersDay['prices']):
                st.markdown(f"**{ticker}**")
                st.markdown(f"Preço: R${price:.2f}")
        
        # Exibição das Maiores Baixas
        with col2:
            st.subheader("Maiores Baixas")
            for ticker, price in zip(top_losers.topLosersDay['tickers'], top_losers.topLosersDay['prices']):
                st.markdown(f"**{ticker}**")
                st.markdown(f"Preço: R${price:.2f}")

top_gainers = GetTopGainers(topGainers)
top_losers = GetTopLosers(topGainers)


def exibir_metricas_e_grafico_ibovespa():
    """
    Exibe o gráfico do IBOVESPA e as métricas dos índices globais e moedas ao lado.
    """
    # Obter dados do IBOVESPA
    dados_ibovespa = obter_dados_indice('^BVSP', periodo="1y")
    close_ibovespa, variacao_ibovespa = calcular_variacao(dados_ibovespa)
    
    # Exibir gráfico do IBOVESPA
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"{close_ibovespa:.0f} | {variacao_ibovespa}%")
        
        gerar_grafico(dados_ibovespa)


    indices_globais = {
        'S&P500' : '^GSPC', 
        'NASDAQ' : '^IXIC',
        'STOXX': '^STOXX',
        'Nikkei': '^N225'
    }
    
    # Obter dados das moedas
    moedas = {
        'Dólar': 'USDBRL=X',  # Ticker do dólar em relação ao real
        'Euro': 'EURBRL=X'   # Ticker do euro em relação ao real
    }
    
    with col2:
        st.image("images/world_map.svg", use_column_width=True)

        col1, col2 = st.columns(2)
        with col1:             
            for titulo, ticker in indices_globais.items():
                dados = obter_dados_indice(ticker, periodo="6mo")
                close, variacao = calcular_variacao(dados)
                st.metric(label=f'{titulo}', value=f"{close:.0f}")

            for titulo, ticker in moedas.items():
                dados = obter_dados_indice(ticker, periodo="6mo")
                close, variacao = calcular_variacao(dados)
                st.metric(label=f'{titulo}', value=f"R${close:.2f}")

            # st.metric(label='bitcoin', value=exibir_valores())

        
        with col2:
            for titulo, ticker in indices_globais.items():
                dados = obter_dados_indice(ticker, periodo="6mo")         
                close, variacao = calcular_variacao(dados)
                st.metric(label="", value=f"{variacao:.2f}%")



            for titulo, ticker in moedas.items():
                dados = obter_dados_indice(ticker, periodo="6mo")
                close, variacao = calcular_variacao(dados)
                st.metric(label="", value=f"{variacao:.2f}%")
                

def main():
    """
    Função principal que organiza o fluxo de execução do aplicativo.
    """
    configurar_pagina()
    exibir_metricas_e_grafico_ibovespa()
    gerar_relatorio(top_gainers, top_losers)


if __name__ == "__main__":
    main()
 