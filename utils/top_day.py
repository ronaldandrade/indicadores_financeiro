"""
API Ibovespa page
https://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/ibov
"""

import requests
import pandas as pd
import streamlit as st

# Obter os dados da B3
url = 'https://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/ibov'
response = requests.get(url)
topGainers = response.json()

class GetTopGainers:
    def __init__(self, topGainers):
        self.topGainersDay = self._get_top_gainers(topGainers)

    def _get_top_gainers(self, topGainers):
        return {
            'tickers': [topGainers['SctyHghstIncrLst'][i]['symb'] for i in range(5)],
            'prices': [topGainers['SctyHghstIncrLst'][i]['SctyQtn']['curPrc'] for i in range(5)]
        }

class GetTopLosers:
    def __init__(self, topGainers):
        self.topLosersDay = self._get_top_losers(topGainers)

    def _get_top_losers(self, topGainers):
        return {
            'tickers': [topGainers['SctyHghstDrpLst'][i]['symb'] for i in range(5)],
            'prices': [topGainers['SctyHghstDrpLst'][i]['SctyQtn']['curPrc'] for i in range(5)]
        }


