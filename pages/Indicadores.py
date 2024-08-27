import streamlit as st
import pandas as pd
import yfinance as yf
from babel.numbers import format_currency
from datetime import datetime
from streamlit_extras.grid import grid
from streamlit_extras.metric_cards import style_metric_cards


# Função para construir a barra lateral
def build_sidebar():
    ticker_list = pd.read_csv("assets/tickers_ibra.csv", index_col=0)
    ticker = st.selectbox(label="Selecione a Empresa", options=ticker_list, placeholder='Códigos')
    ticker = ticker + ".SA"
    start_date = st.date_input("De",format= 'DD/MM/YYYY', value=datetime(2023, 6, 1))
    end_date = st.date_input("Até",format='DD/MM/YYYY', value=datetime.today())
    return ticker, start_date, end_date

# Função para buscar os dados financeiros
def fetch_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    financial_data = {
        'Ticker': ticker,
        'ROE': info.get('returnOnEquity', None),
        'EBITDA': info.get('ebitda', None),
        'P/E Ratio': info.get('trailingPE', None),
        'P/B Ratio': info.get('priceToBook', None),
        'Dividend Yield': info.get('dividendYield', None),
        'Market Cap': info.get('marketCap', None),
        'Debt to Equity': info.get('debtToEquity', None),
    }

    return financial_data

# Função para formatar como porcentagem
def format_as_percentage(number):
    if pd.isna(number):
        return number  # Retorna NaN se o valor for NaN
    return f"{number * 100:.2f}%"

# Função para formatar como moeda
def format_as_currency_babel(number):
    if pd.isna(number):
        return number  # Retorna NaN se o valor for NaN
    return format_currency(number, 'BRL', locale='pt_BR')

# Função para formatar os dados financeiros
def format_data(ticker):
    if ticker:
        # Busca e apresenta os dados financeiros
        data = fetch_financial_data(ticker)
        if data:            
            # Convertendo valores numéricos em porcentagens ou moeda quando necessário
            if data['ROE'] is not None:
                data['ROE'] = format_as_percentage(data['ROE'])
            if data['Dividend Yield'] is not None:
                data['Dividend Yield'] = format_as_percentage(data['Dividend Yield'])
            if data['P/E Ratio'] is not None:
                data['P/E Ratio'] = f"{data['P/E Ratio']:.2f}"
            if data['Market Cap'] is not None:
                data['Market Cap'] = format_as_currency_babel(data['Market Cap'])
            if data['EBITDA'] is not None:
                data['EBITDA'] = format_as_currency_babel(data['EBITDA'])    
            if data['Debt to Equity'] is not None:
                data['Debt to Equity'] = f"{data['Debt to Equity']:.2f}"
                
            # Apresentando os dados em um dataframe
            df = pd.DataFrame(data.items(), columns=['Indicador', 'Valor'])
            # st.dataframe(df)
            mygrid = grid(5, 5, 5, 5, 5, vertical_align="top")

            for index, row in df.iterrows():
               c = mygrid.container()
               c.subheader(row['Indicador'], divider='red')
            #    colA, colB = c.columns(2)
            #    colA.metric(label='Indicador', value=row['Indicador'])
            #    colB.metric(label='Valor', value=row['Valor'])
               c.metric(label=row['Indicador'], value=row['Valor'])
               style_metric_cards(background_color='rgba(255,255,255,0)')
        else:
            st.error('Não foi possível obter os dados financeiros para o ticker fornecido.')


st.set_page_config(layout="wide")

with st.sidebar:

    ticker, start_date, end_date = build_sidebar()

st.title('Indicadores de Desempenho')

# Buscar os dados de fechamento
if ticker:
    prices = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]
    format_data(ticker)
    st.subheader(f'Preços de Fechamento de {ticker}')
    st.line_chart(prices)
